# Python SSRS API

Python implementation of the SSRS API that allows to list, add, edit, delete folders, datasources and reports on an SSRS server.

---
## Initiate api with basic auth

```python
import pySSRSapi

# basic auth
api = pySSRSapi.Api(
    url = 'http://localhost/Reports/api/v2.0',
    user = 'username',
    password = 'password'
)
```

---

## User

### Get current user

```python
user = api.getUser()
```

---

## System

### Get system info

```python
system = api.getSystem()
```

---

## Folders

### Get folders

```python
# list folders
folders = api.getFolders()

# get folder by id
folder = api.getFolderById(id='00000000-0000-0000-0000-000000000000')

# get folder by path
folder = api.getFolderByPath(path='/folder1')

# get root folder
folder = api.getRootFolder()
```

### Add folder

```python
# get root folder for parent folder id
rootFolder = api.getRootFolder()

# initiate new folder
newFolder = pySSRSapi.Folder(
    Id=None,
    Name='folder1',
    Description='Description folder 1',
    Path='/folder1',
    ParentFolderId=rootFolder.Id
)

# add new folder
addedFolder = api.addFolder(folder=newFolder)
```

### Edit folder

```python
# get folder to edit
folder = api.getFolderByPath(path='/folder1')

# modify values
folder.Description = 'Folder 1 desc'

# edit folder
editedFolder = api.editFolder(id=folder.Id, folder=folder)
```

### Set folder policies

```python
# get folder
folder = api.getFolderByPath(path='/folder1')

# initiate policies
policies = dict(
    InheritParentPolicy=False,
    Policies=[
        dict(
            GroupUserName='SERVER\\user_ssrs_1',
            Roles=[
                dict(
                    Name='Report Builder',
                    Description=None
                )
            ]
        )
    ]
)

# set folder policies
api.setFolderPolicies(id=folder.Id, policies=policies)
```

### Delete folder

```python
# get folder to edit
folder = api.getFolderByPath(path='/folder1')

# delete folder
api.deleteFolder(id=folder.Id)
```

---

## Datasources

### Get datatources

```python
# list datasources
datasources = api.getDatasources()

# get datasource by id
datasource = api.getDatasourceById(id='00000000-0000-0000-0000-000000000000')

# get datasource by path
datasource = api.getDatasourceByPath(path='/folder1/datasource1')
```

### Add datasource

```python
# get folder to edit
folder = api.getFolderByPath(path='/folder1')

# get rds file in b64 json friendly
with open('datasource1.rds', 'rb') as f:
    byte_content = f.read()
base64_bytes = base64.b64encode(byte_content)
file_content = base64_bytes.decode('utf-8')

# initiate new datasource
newDatasource = pySSRSapi.Datasource(
    Id=None,
    Name='datasource1',
    Description='Description datasource 1',
    Path='/folder1/datasource1',
    ParentFolderId=folder.Id,
    DataSourceType='ODBC',
    ConnectionString='Dsn=DATASOURCE_1_ODBC_CONNECTION',
    Content=file_content
)

# add new datasource
addedDatasource = api.addDatasource(datasource=newDatasource)
```

### Edit datasource

```python
# get datasource to edit
datasource = api.getDatasourceByPath(path='/folder1/datasource1')

# modify values
datasource.Description = 'Datasource 1 desc'

# edit datasource
editedDatasource = api.editDatasource(id=datasource.Id, datasource=datasource)
```

### Set datasource policies

```python
# get datasource
datasource = api.getDatasourceByPath(path='/folder1/datasource1')

# initiate policies
policies = dict(
    InheritParentPolicy=False,
    Policies=[
        dict(
            GroupUserName='SERVER\\user_ssrs_1',
            Roles=[
                dict(
                    Name='Report Builder',
                    Description=None
                )
            ]
        )
    ]
)

# set datasource policies
api.setDatasourcePolicies(id=datasource.Id, policies=policies)
```

### Delete datasource

```python
# get datasource to edit
datasource = api.getDatasourceByPath(path='/folder1/datasource1')

# delete datasource
api.deleteDatasource(id=datasource.Id)
```

---

## Reports

### Get reports

```python
# list reports
reports = api.getReports()

# get report by id
report = api.getReportById(id='00000000-0000-0000-0000-000000000000')

# get report by path
report = api.getReportByPath(path='/folder1/report1')
```

### Add report

```python
# get folder to edit
folder = api.getFolderByPath(path='/folder1')

# get rds file in b64 json friendly
with open('report1.rdl', 'rb') as f:
    byte_content = f.read()
base64_bytes = base64.b64encode(byte_content)
file_content = base64_bytes.decode('utf-8')

# initiate new report
newReport = pySSRSapi.Report(
    Id=None,
    Name='report1',
    Description='Description report 1',
    Path='/folder1/report1',
    ParentFolderId=folder.Id,
    Content=file_content
)

# add new report
addedReport = api.addReport(report=newReport)
```

### Edit report

```python
# get report to edit
report = api.getReportByPath(path='/folder1/report1')

# modify values
report.Description = 'Report 1 desc'

# edit report
editedReport = api.editReport(id=report.Id, datasource=report)
```

### Set report policies

```python
# get report
report = api.getReportByPath(path='/folder1/report1')

# initiate policies
policies = dict(
    InheritParentPolicy=False,
    Policies=[
        dict(
            GroupUserName='SERVER\\user_ssrs_1',
            Roles=[
                dict(
                    Name='Report Builder',
                    Description=None
                )
            ]
        )
    ]
)

# set report policies
api.setReportPolicies(id=report.Id, policies=policies)
```

### Delete report

```python
# get report to edit
report = api.getReportByPath(path='/folder1/report1')

# delete report
api.deleteReport(id=report.Id)
```