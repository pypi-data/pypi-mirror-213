# Reconify PIP module

The Reconify module is used for sending data to the Reconify platform at [www.reconify.com](https://www.reconify.com). 

Currently the module supports processing and analyzing Chats and Completions from OpenAI. 
Support for additional actions and providers will be added.

## Get started
The first step is to create an account at [app.reconify.com](https://app.reconify.com).

## Generate API and APP Keys
In the Reconify console, add an Application to your account. This will generate both an API_KEY and an APP_KEY 
which will be used in the code below to send data to Reconify.

## Install the module

```
pip install reconify
```

## Integrate the module in code

### Import the module
```python
from reconify import reconifyOpenAIHandler
```

### Initialize the module
Prior to initializing the Reconify module, make sure to import the OpenaAI module.

```python
import openai
openai.api_key = 'YOUR_OPENAI_KEY'
```

Configure the instance of Reconify passing the OpenAi instance along with the Reconify API_KEY and APP_KEY created above.

```python
reconifyOpenAIHandler.config(openai, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key'
)
```

This is all that is needed for a basic integration. The module takes care of sending the correct data to Reconify when you call openai.Completion.create or openai.ChatCompletion.create. 

There are additional optional parameters as well:

### Optional methods

You can optionally pass in a user object or session ID to be used in the analytics reporting. 
The session ID will be used to group interactions together in the same session transcript.

#### Set a user
The user JSON should include a unique userId, all the other fields are optional. 
Without a unique userId, each user will be treated as a new user.

```python
reconifyOpenAIHandler.setUser ({
   "userId": "ABC123",
   "isAuthenticated": 1,
   "firstName": "Francis",
   "lastName": "Smith",
   "email": "",
   "phone": "",
   "gender": "female"
})
```

#### Set a Session ID
The Session ID is an alphanumeric string.
```python
reconifyOpenAIHandler.setSession('MySessionId')
```

#### Set Session Timeout
Set the session timeout in minutes to override the default
```python
reconifyOpenAIHandler.setSessionTimeout(15)
```

## Examples

### Chat Example

```python
import os
import openai
from reconify import reconifyOpenAIHandler

openai.api_key = 'YOUR_OPENAI_KEY'

reconifyOpenAIHandler.config(openai, 'Your_App_Key', 'Your_Api_Key')

reconifyOpenAIHandler.setUser({
   "userId": "12345",
   "isAuthenticated": 1,
   "firstName": "Jim",
   "lastName": "Stand",
   "gender": "male"
})

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an expert on commedians."},
        {"role": "user", "content": "Tell a joke about cats"},
    ],
    temperature=0,
)
```

### Completion Example

```python
import os
import openai
from reconify import reconifyOpenAIHandler

openai.api_key = 'YOUR_OPENAI_KEY'

reconifyOpenAIHandler.config(openai, 'Your_App_Key', 'Your_Api_Key')

reconifyOpenAIHandler.setUser({
   "userId": "12345",
   "isAuthenticated": 1,
   "firstName": "Jim",
   "lastName": "Stand",
   "gender": "male"
})

response = openai.Completion.create(
   model = "text-davinci-003",
   prompt = "write a haiku about cats",
   max_tokens = 100,
   temperature = 0,
)
```
