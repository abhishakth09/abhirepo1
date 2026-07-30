# 1. Connect to Microsoft Entra ID with Role Management permissions
Connect-MgGraph -Scopes "RoleManagement.ReadWrite.Directory"

# 2. Get User Object ID and Global Reader Role Template ID
$User = Get-MgUser -UserId "abi2@entraga.onmicrosoft.com"
$RoleDefinition = Get-MgRoleManagementDirectoryRoleDefinition -Filter "displayName eq 'Global Reader'"

# 3. Assign Role Directly as Active
$params = @{
    "@odata.type" = "#microsoft.graph.unifiedRoleAssignment"
    "principalId" = $User.Id
    "roleDefinitionId" = $RoleDefinition.Id
    "directoryScopeId" = "/"
}

New-MgRoleManagementDirectoryRoleAssignment -BodyParameter $params