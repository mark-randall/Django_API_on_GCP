#!/bin/bash

create_service_account()
{
    PROJECT_ID=$DEVSHELL_PROJECT_ID
    SERVICE_NAME=$1
    SA=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

    # Check if SA exists
    # Create if necessary
    EXISTING_SA=$(gcloud iam service-accounts list)
    if ! [[ "$EXISTING_SA" == *"$SA"* ]]; then
        gcloud iam service-accounts create $SERVICE_NAME --display-name "$SERVICE_NAME service account"
        echo "Service Account created with name: $SA" 
    else
        echo "$SA already exists"
    fi

    for role in cloudsql.client run.admin; do
        gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$SA --role roles/${role}
    done
}

deploy() 
{
    PROJECT_ID=$DEVSHELL_PROJECT_ID
    SERVICE_NAME=$1
    SA=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

    # Create service account if necessary
    EXISTING_SA=$(gcloud iam service-accounts list)
    if ! [[ "$EXISTING_SA" == *"$SA"* ]]; then
        $(create_service_account())
    fi

    # Create container and add to Container Registry
    gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME .

    # Deploy conntainer to Cloud Run
    gcloud run deploy $SERVICE_NAME --allow-unauthenticated --image gcr.io/$PROJECT_ID/$SERVICE_NAME --service-account $SA

    # Set ENV VAR for Django ALLOWED_HOSTS
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --format "value(status.url)")
    gcloud run services update $SERVICE_NAME --update-env-vars "CURRENT_HOST=${SERVICE_URL}"
}