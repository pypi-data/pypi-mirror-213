# DSM Email

## install
```
pip install dsmemail
```

## how to use
1. set env

```
DSM_EMAIL_URI=<DSM_EMAIL_URI>
DSM_EMAIL_APIKEY=<DSM_EMAIL_APIKEY>
```

2. send email

```python
import dsmemail

status, msg = dsmemail.sendEmail(
    subject="test", 
    message="helloworld", 
    emails=["admin@admin.com"],
    attachments=["test.txt"]
)
print(status, msg)
```
| variable      | dtype      | description                           |
| --------      | ---------  | ------------------------------------- |
| subject       | str        | subject of email                      |
| message       | str        | email body can contains html string   |
| emails        | List[str]  | email to send message                 |
| attachments   | List[str]  | list of filepath(str) to attach files   | 

output
```
(True, 'email send sucess')
```

#
status
```
True = send email sucess
False = send email fail
```

msg
```
string describe status
```