import boto3


def lambda_handler(context, event):

    client = boto3.client("iam")
    sns = boto3.client("sns")
    response = client.list_users()
    userVirtualMfa = client.list_virtual_mfa_devices()
    mfaNotEnabled = []
    physicalString = ""

    # loop through users to find physical MFA
    for user in response["Users"]:
        userMfa = client.list_mfa_devices(UserName=user["UserName"])

        if len(userMfa["MFADevices"]) == 0:
                mfaNotEnabled.append(user["UserName"])

    if len(mfaNotEnabled) > 0:
        physicalString = " MFA is Disabled\n\n" "\n".join(mfaNotEnabled)
    else:
        physicalString = "All Users have MFA enabled"

    response = sns.publish(
        TopicArn="ARN_HERE",
        Message=physicalString,
        Subject="MFA Disabled Check",
    )

    return mfaNotEnabled
