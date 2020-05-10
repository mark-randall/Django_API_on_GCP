#!/bin/bash

PROJECT_ID=django-api-276715 #$DEVSHELL_PROJECT_ID

create_service_account()
{ 
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

random_password() 
{
    echo $(openssl rand -base64 16)
}

create_db()
{
    SERVICE_NAME=$1
    SA=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
    REGION=us-central1
    DB_ROOT_PASSWORD=$(random_password)
    DB_USER_NAME=db_user
    DB_USER_PASSWORD=$(random_password)

    # Create SQL 
    gcloud config set project $PROJECT_ID
    gcloud sql instances create $SERVICE_NAME --database-version POSTGRES_11 --tier db-f1-micro --region $REGION --project $PROJECT_ID --root-password $DB_ROOT_PASSWORD
    
    # Create DB
    gcloud sql databases create $SERVICE_NAME --instance=$SERVICE_NAME
    
    # Create DB user
    gcloud sql users create $DB_USER_NAME --password $DB_USER_PASSWORD --instance $SERVICE_NAME

    DATABASE_URL=postgres://$DB_USER_NAME:$DB_USER_PASSWORD@//cloudsql/$PROJECT_ID:$REGION:$SERVICE_NAME/$SERVICE_NAME

    # Save full DB URL to Cloud Secrete Mangaer with key DB_URL
    DB_URL_KEY=DATABASE_URL
    gcloud secrets create $DB_URL_KEY --replication-policy automatic
    echo -n "${DATABASE_URL}" | gcloud secrets versions add $DB_URL_KEY --data-file=-

    gcloud secrets add-iam-policy-binding $DB_URL_KEY --member serviceAccount:$SA --role roles/secretmanager.secretAccessor
}

deploy() 
{
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