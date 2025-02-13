"""Module to deploy to staging EB environment."""
import boto3
import time
elasticbeanstalk = boto3.client('elasticbeanstalk')
servicecatalog = boto3.client('servicecatalog')
terminate_time = 720
eb_app_name = "VariationNormalization"
eb_env_name = "VariationNormalization-dev-env"
sc_product_id = "prod-mmw6ymv2ntzl2"
print(f'Launching new Service Catalog Product for dev environment: '
      f'{eb_app_name}')
sc_product_artifacts = \
    servicecatalog.list_provisioning_artifacts(ProductId=sc_product_id)
for artifact in sc_product_artifacts['ProvisioningArtifactDetails']:
    if artifact['Active']:
        provisioning_artifact_id = artifact['Id']
try:
    eb_provisioned_product = \
        servicecatalog.provision_product(
            ProductId=sc_product_id,
            ProvisioningArtifactId=provisioning_artifact_id,
            ProvisionedProductName=eb_env_name,
            ProvisioningParameters=[
                {
                    'Key': 'Env',
                    'Value': eb_app_name
                },
                {
                    'Key': 'EnvType',
                    'Value': 'dev'
                },
                {
                    'Key': 'TerminateTime',
                    'Value': str(terminate_time)
                }
            ])
    eb_provisioned_product_Id = \
        eb_provisioned_product['RecordDetail']['ProvisionedProductId']
    product_status = \
        servicecatalog.describe_provisioned_product(
            Id=eb_provisioned_product_Id)
    eb_provisioned_product_status = \
        product_status['ProvisionedProductDetail']['Status']
    while eb_provisioned_product_status == "UNDER_CHANGE":
        time.sleep(10)
        product_status = \
            servicecatalog.describe_provisioned_product(
                Id=eb_provisioned_product_Id)
        eb_provisioned_product_status = \
            product_status['ProvisionedProductDetail']['Status']
        print(eb_provisioned_product_status)
except Exception as e:  # noqa: E722
    print(e)
    print("The EB environment is already running....")
