mock_javascript_val="""
Sure! Here's a simple JavaScript code snippet that demonstrates how to create a basic calculator that adds, subtracts, multiplies, and divides two numbers. This example includes HTML and JavaScript.

```html
<!DOCTYPE html>
<html lang=&quot;en&quot;>
<head>
    <meta charset=&quot;UTF-8&quot;>
    <meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;>
    <title>Simple Calculator</title>
</head>
<body>
    <h1>Simple Calculator</h1>
    <input type=&quot;number&quot; id=&quot;num1&quot; placeholder=&quot;Enter first number&quot;>
    <input type=&quot;number&quot; id=&quot;num2&quot; placeholder=&quot;Enter second number&quot;>
    
    <div>
        <button onclick=&quot;calculate('add')&quot;>Add</button>
        <button onclick=&quot;calculate('subtract')&quot;>Subtract</button>
        <button onclick=&quot;calculate('multiply')&quot;>Multiply</button>
        <button onclick=&quot;calculate('divide')&quot;>Divide</button>
    </div>
    
    <h2 id=&quot;result&quot;>Result: </h2>

    <script>
        function calculate(operation) {
            const num1 = parseFloat(document.getElementById(&quot;num1&quot;).value);
            const num2 = parseFloat(document.getElementById(&quot;num2&quot;).value);
            let result;

            switch (operation) {
                case 'add':
                    result = num1 + num2;
                    break;
                case 'subtract':
                    result = num1 - num2;
                    break;
                case 'multiply':
                    result = num1 * num2;
                    break;
                case 'divide':
                    result = num2 !== 0 ? num1 / num2 : 'Cannot divide by zero';
                    break;
                default:
                    result = 'Invalid operation';
            }

            document.getElementById(&quot;result&quot;).innerText = &quot;Result: &quot; + result;
        }
    </script>
</body>
</html>
```

### How to Use:
1. Copy the code into a text editor and save it as `calculator.html`.
2. Open the file in a web browser.
3. Enter two numbers in the input fields and click any of the operation buttons to see the result.

This simple calculator allows you to perform basic arithmetic operations and shows the result on the webpage.
"""
