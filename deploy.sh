#!/bin/bash

# Environment vars required to call one or more deploy methods
# PROJECT_ID: GCP Project ID
# PROJECT_NUMBER: GCP Project Number
# 
# SERVICE_NAME: Service name. Used as Deployment Manager deployment name
# REGION: GCP Region
# DATABASE_USER_PASSWORD: Password for service specific DB user
#
# REPO_NAME: Github repo name
# REPO_OWNER: Github username

# Creates infastructure for project
deploy_infastructure() 
{
    # Use GCP Deployment Manager to create infastructure for project
    # SEE: template.jinja 
    gcloud deployment-manager deployments update $SERVICE_NAME \
        --template deployment_manager/template.jinja \
        --properties db-user-password:$DATABASE_USER_PASSWORD,region:$REGION

    # Add secrets to secret manager
    # Not possible with Deployment Manager

    # Bucket name
    GS_BUCKET_NAME=$PROJECT_ID-$SERVICE_NAME
    gcloud secrets create GS_BUCKET_NAME --replication-policy automatic
    echo -n "${GS_BUCKET_NAME}" | gcloud secrets versions add GS_BUCKET_NAME --data-file=-

    # Database connection URL
    DATABASE_URL=postgres://$SERVICE_NAME:$DATABASE_USER_PASSWORD@//cloudsql/$PROJECT_ID:$REGION:$SERVICE_NAME-sql/$SERVICE_NAME
    gcloud secrets create DATABASE_URL --replication-policy automatic
    echo -n "${DATABASE_URL}" | gcloud secrets versions add DATABASE_URL --data-file=-
}

# First deployment
# Only necessary to call once
deploy_first() 
{
    SERVICE_ACCOUNT=$SERVICE_NAME@$PROJECT_ID.iam.gserviceaccount.com

    # Build and deploy app with Cloud Build
    # Step deploys to Cloud Run
    # SEE: cloud-build.yaml 
    gcloud builds submit \
        --config cloud_build/cloud-build.yaml \
        --substitutions "_REGION=${REGION},_SQL_INSTANCE_NAME=${SERVICE_NAME}-sql,_SERVICE_NAME=${SERVICE_NAME},_SERVICE_ACCOUNT=${SERVICE_ACCOUNT}"

    # Set ENV VAR for Django ALLOWED_HOSTS
    # SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --format "value(status.url)")
    # gcloud run services update $SERVICE_NAME \
    #     --update-env-vars "CURRENT_HOST=${SERVICE_URL}"  
}

# Setup for future deployments
# Only necessary to call once
deploy_trigger() 
{
    # Setup git trigger 
    # Deploys on push to master branch
    gcloud beta builds triggers create github \
        --repo-name $REPO_NAME \
        --repo-owner $REPO_OWNER \
        --branch-pattern master \
        --build-config cloud_build/cloud-build.yaml \
        --substitutions "_REGION=${REGION},_SQL_INSTANCE_NAME=${SERVICE_NAME}-sql,_SERVICE_NAME=${SERVICE_NAME},_SERVICE_ACCOUNT=${SERVICE_ACCOUNT}"
}