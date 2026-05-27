# Serverless Web App
### AWS S3 | API Gateway | Lambda | DynamoDB

---

## What This Is

A serverless web application where a user fills out a form on a static 
website. The form submission is processed by a Lambda function through 
API Gateway and the data is stored in DynamoDB. 

No server is running at any point. The entire backend only executes 
when a user submits the form.

---

## Architecture

| Service | Role | Why This Service |
|---|---|---|
| S3 | Hosts the static frontend HTML file | Serves files without a running server. Zero management, infinite scale, near-zero cost |
| API Gateway | Receives HTTP requests from the browser | Lambda has no public URL. API Gateway sits on the internet and routes requests internally |
| Lambda | Processes the form submission | Runs only when triggered. No idle cost. No server to manage or patch |
| DynamoDB | Stores the submitted data | Serverless database. No provisioning required. Scales automatically |
| IAM | Controls what Lambda is allowed to do | Lambda is restricted to only what it needs — DynamoDB write and CloudWatch logging |
| CloudWatch | Captures Lambda execution logs | Visibility into every function invocation |

---

## How It Works

1. A user opens the website URL in their browser

2. The browser requests the HTML file from S3

3. S3 returns the HTML file with no code runs, S3 just delivers the file

4. The user fills in the form and clicks submit

5. The JavaScript in the HTML sends a POST request to the API Gateway URL

6. API Gateway receives the request and triggers the Lambda function

7. Lambda reads the form data from the request

8. Lambda writes the data to DynamoDB

9. Lambda returns a success response to API Gateway

10. API Gateway sends that response back to the browser

11. The user sees a confirmation message

---

## Security and Permissions

**Lambda IAM Role (Least Privilege)**

The Lambda function runs under a dedicated IAM role with exactly 
two permissions attached.

- Write items to the FormSubmissions DynamoDB table
- Write logs to CloudWatch Logs

No other permissions are attached. If the function is ever 
compromised, the blast radius is limited to those two actions only.

---

## Lessons Learnt and Troubleshooting

Building a completely serverless backend was a great exercise in 
connecting moving parts. Since there is no traditional server to 
log into, I relied heavily on CloudWatch logs to catch issues 
during development.

---

**The Typo Trap (Debugging a Python NameErro)r**

What happened: I hit a NameError because I accidentally typed 
`sudmission_Id` when creating the variable, but tried to reference 
it as `submission_id` later in the code. Python could not find it 
because they are two different names.

How I fixed it: I matched the variable names exactly across the 
script and adopted snake_case as a consistent naming convention 
going forward.

---

**Case-Sensitivity in AWS Resource Names**

What happened: My Lambda function could not write to DynamoDB. 
It kept throwing an error because I wrote the table name as 
`form-submissions` in my code while the actual table in AWS 
was named `FormSubmissions`.

How I fixed it: AWS treats all resource names with strict 
case-sensitivity. I updated the code to match the exact casing 
of the deployed table and the connection was immediately restored.

---

**DynamoDB Partition Key Strict Matching**

What happened: Even after fixing the table name, DynamoDB rejected 
my data. I used `submissionid` in my payload but the partition key 
defined in the table was `submissionId` with a capital I.

How I fixed it: DynamoDB is strict about primary keys. If the 
casing does not match the schema exactly the write fails. I matched 
the payload key to the exact partition key name and submissions 
started going through immediately.

---

## What I Would Do Differently

**Stricter IAM policy**

Instead of `AmazonDynamoDBFullAccess` I would write a custom policy 
restricting Lambda to `PutItem` on the FormSubmissions table ARN only.

**Input validation in Lambda**

If someone calls the API without a body the function crashes with 
an unhandled exception. I would add error handling to return a 
meaningful error response instead.

**Replace the CORS wildcard**

`Access-Control-Allow-Origin: *` allows any website to call my API. 
In production I would replace this with my specific domain only.

---

## Future Improvements

- Custom IAM policy restricting Lambda to PutItem on the 
  FormSubmissions table ARN only

- API Gateway rate limiting or WAF to prevent endpoint abuse

- Input validation in Lambda including max length checks 
  and format validation

- Structured JSON logging in CloudWatch including request 
  ID and timestamp

- Frontend loading spinner and disabled submit button 
  during request processing

- DynamoDB encryption at rest explicitly configured

---

## Project Status
Completed

---

## Author

Chinukwue Doris

[GitHub Profile](https://github.com/Doris-Chinukwue)