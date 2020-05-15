#!/bin/bash

PROJECT_ID=$DEVSHELL_PROJECT_ID

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

    gcloud iam service-accounts add-iam-policy-binding ${SA} --member "serviceAccount:${CLOUDBUILD_SA}" --role "roles/iam.serviceAccountUser"
}

random_password() 
{
    echo $(openssl rand -base64 16)
}

create_db()
{
    SERVICE_NAME=$1
    DB_VERSION=$2
    SQL_INSTANCE_NAME=${1}-${2}
    SA=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
    REGION=us-central1
    DB_ROOT_PASSWORD=$(random_password)
    DB_USER_NAME=db_user
    DB_USER_PASSWORD=$(random_password)

    # Create SQL 
    gcloud config set project $PROJECT_ID
    gcloud sql instances create $SQL_INSTANCE_NAME --database-version POSTGRES_11 --tier db-f1-micro --region $REGION --project $PROJECT_ID --root-password $DB_ROOT_PASSWORD
    
    # Create DB
    gcloud sql databases create $SERVICE_NAME --instance=$SQL_INSTANCE_NAME
    
    # Create DB user
    gcloud sql users create $DB_USER_NAME --password $DB_USER_PASSWORD --instance $SQL_INSTANCE_NAME

    DATABASE_URL=postgres://$DB_USER_NAME:$DB_USER_PASSWORD@//cloudsql/$PROJECT_ID:$REGION:$SQL_INSTANCE_NAME/$SERVICE_NAME

    # Save full DB URL to Cloud Secrete Mangaer with key DB_URL
    DB_URL_KEY=DATABASE_URL
    gcloud secrets create $DB_URL_KEY --replication-policy automatic
    echo -n "${DATABASE_URL}" | gcloud secrets versions add $DB_URL_KEY --data-file=-

    gcloud secrets add-iam-policy-binding $DB_URL_KEY --member serviceAccount:$SA --role roles/secretmanager.secretAccessor
}

create_storage()
{
    SERVICE_NAME=$1
    SA=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
    REGION=us-central1
    GS_BUCKET_NAME=${PROJECT_ID}-media

    gsutil mb -l ${REGION} gs://${GS_BUCKET_NAME}
    gsutil iam ch serviceAccount:${SA}:roles/storage.objectAdmin gs://${GS_BUCKET_NAME} 

    BUCKET_NAME_KEY=GS_BUCKET_NAME
    gcloud secrets create $BUCKET_NAME_KEY --replication-policy automatic
    echo -n "${GS_BUCKET_NAME}" | gcloud secrets versions add $BUCKET_NAME_KEY --data-file=-

    gcloud secrets add-iam-policy-binding $BUCKET_NAME_KEY --member serviceAccount:$SA --role roles/secretmanager.secretAccessor
}

deploy() 
{
    SERVICE_NAME=$1
    DB_VERSION=$2
    SQL_INSTANCE_NAME=${1}-${2}
    SA=${SERVICE_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
    REGION=us-central1
    GS_BUCKET_NAME=${PROJECT_ID}-media

    # Create service account if necessary
    EXISTING_SA=$(gcloud iam service-accounts list)
    if ! [[ "$EXISTING_SA" == *"$SA"* ]]; then
        $(create_service_account() $SERVICE_NAME)
    fi

    # Create GCS account if necessary
    EXISTING_BUCKETS=$(gsutil list)
    if ! [[ "$EXISTING_BUCKETS" == *"$GS_BUCKET_NAME"* ]]; then
        $(create_storage() $SERVICE_NAME)
    fi

    # Create DB if necessary
    EXISTING_SQL=$(gcloud sql instances list)
    if ! [[ "$EXISTING_SQL" == *"$SERVICE_NAME"* ]]; then
        $(create_db() $SERVICE_NAME $DB_VERSION)
    fi

    # Create container and add to Container Registry
    gcloud builds submit --config cloud-build.yaml --substitutions "_REGION=${REGION},_SQL_INSTANCE_NAME=${SQL_INSTANCE_NAME},_SERVICE_NAME=${SERVICE_NAME}"

    # Deploy conntainer to Cloud Run
    #gcloud run deploy $SERVICE_NAME --allow-unauthenticated --image gcr.io/$PROJECT_ID/$SERVICE_NAME --service-account $SA

    # Set ENV VAR for Django ALLOWED_HOSTS
    # Set SQL instance
    #SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --format "value(status.url)")
    #gcloud run services update $SERVICE_NAME --update-env-vars "CURRENT_HOST=${SERVICE_URL}" --set-cloudsql-instances $PROJECT_ID:$REGION:$SQL_INSTANCE_NAME
}

add_deploy_trigger() {

    SERVICE_NAME=$1
    DB_VERSION=$2
    REPO_OWNER=mark-randall
    SQL_INSTANCE_NAME=${1}-${2}
    REGION=us-central1

    gcloud beta builds triggers create github \
        --repo-name django-on-gcp \
        --repo-owner ${REPO_OWNER} \
        --branch-pattern master \
        --build-config cloud-build.yaml \
        --substitutions "_REGION=${REGION},_INSTANCE_NAME=${SQL_INSTANCE_NAME},_SERVICE=${SERVICE_NAME}"
} 

delete()
{
    SERVICE_NAME=$1
    DB_VERSION=$2
    SQL_INSTANCE_NAME=${1}-${2}

    gcloud sql instances delete $SQL_INSTANCE_NAME

    # NOTE: Not deleting run service because it is serverless and scales to zero
    # https://cloud.google.com/run/pricing
    # gcloud beta run services delete $SERVICE_NAME
}