import boto3
import argparse
from botocore.exceptions import ClientError

def get_ec2_client(region_name='us-east-1'):
    """Initialize and return an EC2 client"""
    try:
        # Create a session to check credentials first
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if not credentials or not credentials.access_key:
            print("\nError: No AWS credentials found. Please configure your AWS credentials using one of these methods:")
            print("1. Run 'aws configure'")
            print("2. Set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and optionally AWS_DEFAULT_REGION")
            print("3. Use an IAM role if running on EC2")
            return None
            
        print(f"\nUsing AWS credentials from: {credentials.method.upper()}")
        print(f"AWS Access Key: {credentials.access_key[:4]}...{credentials.access_key[-4:]}")
        print(f"Region: {region_name}")
        
        return boto3.client('ec2', region_name=region_name)
        
    except Exception as e:
        print(f"\nError initializing AWS client: {e}")
        print("Please verify your AWS credentials and region configuration.")
        return None

def check_volume_encryption(ec2_client, volume_id):
    """Check if a volume is encrypted"""
    try:
        response = ec2_client.describe_volumes(VolumeIds=[volume_id])
        if 'Volumes' in response and response['Volumes']:
            return response['Volumes'][0].get('Encrypted', False)
    except ClientError as e:
        print(f"Error checking volume {volume_id}: {e}")
    return False

def list_instances_with_unencrypted_volumes(region):
    """List all EC2 instances and check their EBS volumes for encryption"""
    print("\nAttempting to connect to AWS...")
    ec2_client = get_ec2_client(region)
    if not ec2_client:
        print("\nFailed to initialize EC2 client. Please check your AWS configuration.")
        return

    try:
        print("\nFetching EC2 instances...")
        # Get all instances
        instances = ec2_client.describe_instances()
        
        print(f"\n{'='*80}")
        print(f"Checking EC2 instances in region: {region}")
        print(f"{'='*80}")
        
        for reservation in instances.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_id = instance.get('InstanceId')
                instance_name = next((tag['Value'] for tag in instance.get('Tags', []) 
                                   if tag['Key'] == 'Name'), 'N/A')
                
                print(f"\nInstance ID: {instance_id}")
                print(f"Instance Name: {instance_name}")
                print(f"Instance State: {instance['State']['Name']}")
                
                # Check each volume attached to the instance
                for device in instance.get('BlockDeviceMappings', []):
                    volume_id = device.get('Ebs', {}).get('VolumeId')
                    if volume_id:
                        is_encrypted = check_volume_encryption(ec2_client, volume_id)
                        status = "ENCRYPTED" if is_encrypted else "NOT ENCRYPTED"
                        
                        # Highlight unencrypted volumes in red
                        if not is_encrypted:
                            status = f"\033[91m{status} - WARNING: Unencrypted volume!\033[0m"
                        
                        print(f"  Volume {volume_id}: {status}")
                
                print("-" * 50)
        
        print("\nScan complete!")
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        
        print(f"\nAWS API Error ({error_code}): {error_message}")
        
        if error_code == 'UnauthorizedOperation':
            print("\nRequired IAM permissions for this script:")
            print("1. ec2:DescribeInstances")
            print("2. ec2:DescribeVolumes")
            print("\nPlease ensure your IAM user/role has these permissions.")
            
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check your network connection and AWS configuration.")
    finally:
        print("\nScript execution completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check EBS volume encryption for EC2 instances')
    parser.add_argument('--region', type=str, default='us-east-1', 
                       help='AWS region (default: us-east-1)')
    
    args = parser.parse_args()
    
    print("EC2 Instance EBS Volume Encryption Checker")
    print("=" * 50)
    print("Note: This script requires AWS credentials to be configured")
    print("      (via AWS CLI, environment variables, or IAM role)")
    
    list_instances_with_unencrypted_volumes(args.region)
