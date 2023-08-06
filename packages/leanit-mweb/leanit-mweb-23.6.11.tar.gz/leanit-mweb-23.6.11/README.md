Lean IT Mweb Framework

write a python function which gets a html input. The function should return a Form objects. The Form objects represents data parsed from the html <form> tag. The following code should work:

```python
html = "<html>...</html>"
# Form.parse is a classmethod, stores the html in the form object, parses the action, method and inputs in the __init__ method and manages a data dict with the input values
form = Form.parse(html) 
# if multiple forms are in the html, you can use
# parse_forms(html, index=0) to get the first form
# or parse_forms(html, id="form_id") to get the form with the given id
# or parse_forms(html, name="form_name") to get the form with the given name

form.fill(name="foo") # fill the form with data, updates form.data dict

# submit the form and get the response
# uses e.g. client.get("/workspace/create-first", allow_redirects=False)
# or client.post("/workspace/create-first", allow_redirects=False)
# based on the method and action of the form
response = form.submit(client)
```

Do not use beatifulsoup or other html parsers. Use regex to parse the html.