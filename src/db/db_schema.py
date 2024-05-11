"""
MIT License

Copyright (c) 2024 David Southwood

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
TABLES_SQL = {
    "categories": """CREATE TABLE IF NOT EXISTS [categories] (
                        [id] INTEGER PRIMARY KEY,
                        [name] TEXT NOT NULL,
                        [description] TEXT
                     );""",
    "languages": """CREATE TABLE IF NOT EXISTS [languages] (
                        [id] INTEGER PRIMARY KEY,
                        [name] TEXT NOT NULL
                     );""",
    "languages_categories": """CREATE TABLE IF NOT EXISTS [languages_categories] (
                    [id] INTEGER PRIMARY KEY,
                    [language_id] INTEGER,
                    [category_id] INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(id),
                    FOREIGN KEY (language_id) REFERENCES languages(id)
                 );""",
    "snippets": """CREATE TABLE IF NOT EXISTS [snippets] (
                       [id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       [title] TEXT NOT NULL,
                       [code] TEXT NOT NULL,
                       [language_id] INTEGER,
                       [category_id] INTEGER,
                       [created_at] TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (category_id) REFERENCES categories(id),
                       FOREIGN KEY (language_id) REFERENCES languages(id)
                   );"""
}

INITIAL_DATA_SQL = {
    "languages": [
        """INSERT INTO languages (name) VALUES ('Python');""",
        """INSERT INTO languages (name) VALUES ('JavaScript');""",
        """INSERT INTO languages (name) VALUES ('Java');""",
        """INSERT INTO languages (name) VALUES ('C#');"""
    ],
    "categories": [
        """INSERT INTO categories (name, description) VALUES ('General', 'Covers fundamental and widely applicable programming concepts.');""",
        """INSERT INTO categories (name, description) VALUES ('Data Structures', 'Snippets related to arrays, lists, dictionaries, sets, trees, graphs, queues, stacks, etc.');""",
        """INSERT INTO categories (name, description) VALUES ('Algorithms', 'Sorting, searching, recursion, dynamic programming, graph algorithms, etc.');""",
        """INSERT INTO categories (name, description) VALUES ('Database Operations', 'CRUD operations, connections, transactions, queries, migrations.');""",
        """INSERT INTO categories (name, description) VALUES ('File Handling', 'Reading, writing, parsing, and manipulating files in various formats (e.g., CSV, JSON, XML).');""",
        """INSERT INTO categories (name, description) VALUES ('Networking', 'HTTP requests, sockets, API consumption, web scraping.');""",
        """INSERT INTO categories (name, description) VALUES ('Concurrency', 'Threads, asynchronous programming, parallel execution, locks, semaphores.');""",
        """INSERT INTO categories (name, description) VALUES ('Testing', 'Unit tests, integration tests, mock objects, test-driven development snippets.');""",
        """INSERT INTO categories (name, description) VALUES ('Debugging', 'Logging, profiling, debugging techniques, memory leak detection.');""",
        """INSERT INTO categories (name, description) VALUES ('Security', 'Encryption, hashing, secure storage, XSS prevention, CSRF protection.');""",
        """INSERT INTO categories (name, description) VALUES ('User Interface', 'UI components, layouts, event handling, responsive design.');""",
        # General categories added, now adding placeholders for language-specific categories
        """INSERT INTO categories (name, description) VALUES ('Data Analysis', 'Pandas, NumPy, data visualization (Matplotlib, Seaborn).');""",
        """INSERT INTO categories (name, description) VALUES ('Web Development', 'Flask, Django snippets.');""",
        """INSERT INTO categories (name, description) VALUES ('Machine Learning', 'Scikit-learn, TensorFlow, PyTorch examples.');""",
        """INSERT INTO categories (name, description) VALUES ('Frontend', 'React, Vue, Angular snippets.');""",
        """INSERT INTO categories (name, description) VALUES ('Backend', 'Node.js, Express.js code examples.');""",
        """INSERT INTO categories (name, description) VALUES ('Spring Framework', 'Dependency injection, Spring Boot applications, JPA.');""",
        """INSERT INTO categories (name, description) VALUES ('Android Development', 'Activities, Services, Android UI components.');""",
        """INSERT INTO categories (name, description) VALUES ('.NET Core', 'ASP.NET MVC, Entity Framework Core, middleware.');""",
        """INSERT INTO categories (name, description) VALUES ('Game Development', 'Unity game development snippets.');""",
        """INSERT INTO categories (name, description) VALUES ('Windows Development', 'WPF, UWP examples.');"""
    ],
    "language_specific_categories": [
        # Link Python-specific categories
        """INSERT INTO languages_categories (language_id, category_id) SELECT languages.id, categories.id FROM languages, categories WHERE languages.name = 'Python' AND categories.name IN ('Data Analysis', 'Web Development', 'Machine Learning');""",
        # Link JavaScript-specific categories
        """INSERT INTO languages_categories (language_id, category_id) SELECT languages.id, categories.id FROM languages, categories WHERE languages.name = 'JavaScript' AND categories.name IN ('Frontend', 'Backend');""",
        # Link Java-specific categories
        """INSERT INTO languages_categories (language_id, category_id) SELECT languages.id, categories.id FROM languages, categories WHERE languages.name = 'Java' AND categories.name IN ('Spring Framework', 'Android Development');""",
        # Link C#-specific categories
        """INSERT INTO languages_categories (language_id, category_id) SELECT languages.id, categories.id FROM languages, categories WHERE languages.name = 'C#' AND categories.name IN ('.NET Core', 'Game Development', 'Windows Development');"""
    ],
    "snippets": [
            # Python
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Hello World', 'print("Hello, World!")', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General') );""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('List Comprehension', 'squares = [x**2 for x in range(10)]', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));        """,
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Dictionary Comprehension', '{x: x**2 for x in (2, 4, 6)}', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Function Definition', 'def greet(name):\n    return "Hello, " + name', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Lambda Function', 'double = lambda x: x * 2', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('File Read', 'with open("file.txt") as f:\n    content = f.read()', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('JSON Parsing', 'import json\n\n# Parse JSON\ndata = json.loads(''{"name": "John", "age": 30}'')', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('HTTP GET Request', 'import requests\n\nresponse = requests.get("https://api.example.com/")\ndata = response.json()', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Class Definition', 'class MyClass:\n    x = 5', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Try Except', 'try:\n    print(x)\nexcept NameError:\n    print("Variable x is not defined")', (SELECT id FROM languages WHERE name = 'Python'), (SELECT id FROM categories WHERE name = 'General'));""",
            # Javascipt
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Declaring Variables', 'let name = "CodeKeeper";\nconst YEAR_ESTABLISHED = 2024;\nvar isApplicationActive = true;', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Basic Function', 'function greet(name) {\n  console.log(`Hello, ${name}!`);\n}\ngreet("User");', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Using Arrow Functions', 'const add = (a, b) => a + b;\nconsole.log(add(5, 3));', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Working With Arrays', 'let fruits = ["apple", "banana", "cherry"];\nconsole.log(fruits.length);', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Object Literals', 'const person = {\n  name: "John Doe",\n  age: 30\n};\nconsole.log(person.name);', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Template Literals', 'let personName = "John";\nconsole.log(`Hello, ${personName}!`);', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Destructuring Assignment', 'const user = { id: 100, name: "John Doe" };\nconst { id, name } = user;\nconsole.log(name);', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Spread Operator', 'let parts = ["shoulders", "knees"];\nlet lyrics = ["head", ...parts, "and", "toes"];\nconsole.log(lyrics);', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Promises', 'const myPromise = new Promise((resolve, reject) => {\n  let condition = true;\n  if (condition) {\n    resolve("Promise is resolved.");\n  } else {\n    reject("Promise is rejected.");\n  }\n});', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Async/Await', 'async function fetchData() {\n  let data = await fetch("https://api.example.com");\n  console.log(await data.json());\n}', (SELECT id FROM languages WHERE name = 'JavaScript'), (SELECT id FROM categories WHERE name = 'General'));""",
            # Java
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Hello World', 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Basic Class Definition', 'public class Bicycle {\n    int speed = 0;\n    void speedUp(int increment) {\n        speed += increment;\n    }\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Interfaces', 'interface Animal {\n    public void eat();\n    public void travel();\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Try-Catch', 'try {\n    int[] myNumbers = {1, 2, 3};\n    System.out.println(myNumbers[10]);\n} catch (Exception e) {\n    System.out.println("Something went wrong.");\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Generics', 'public class Box<T> {\n    private T t;\n    public void set(T t) { this.t = t; }\n    public T get() { return t; }\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Enums', 'enum Level {\n    LOW,\n    MEDIUM,\n    HIGH\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Lambda Expressions', 'List<String> names = Arrays.asList("John", "Doe", "Sarah");\nnames.forEach(name -> System.out.println(name));', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Stream API', 'List<Integer> numbers = Arrays.asList(2, 3, 4, 5);\nList<Integer> square = numbers.stream().map(x -> x*x).collect(Collectors.toList());', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Multithreading', 'class MultiThreadDemo extends Thread {\n    public void run() {\n        System.out.println("Thread is running.");\n    }\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES ('Annotations', '@Override\npublic String toString() {\n    return "Override example";\n}', (SELECT id FROM languages WHERE name = 'Java'), (SELECT id FROM categories WHERE name = 'General'));""",
            # C#
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Hello World', 'using System;\nclass Program {\n    static void Main(string[] args) {\n        Console.WriteLine("Hello, World!");\n    }\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Basic Class Definition', 'public class Bicycle {\n    public int Speed { get; set; } = 0;\n    public void SpeedUp(int increment) {\n Speed += increment;\n }\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Interfaces', 'interface IAnimal {\n void Eat();\n void Travel();\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Try-Catch', 'try {\n int[] myNumbers = new int[] {1, 2, 3};\n Console.WriteLine(myNumbers[10]);\n} catch (Exception e) {\n Console.WriteLine("Something went wrong.");\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Generics', 'public class Box<T> {\n private T content;\n public void SetContent(T content) {\n this.content = content;\n }\n public T GetContent() {\n return content;\n }\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Enums', 'enum Level {\n Low,\n Medium,\n High\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Lambda Expressions', 'List<string> names = new List<string> { "John", "Doe", "Sarah" };\nnames.ForEach(name => Console.WriteLine(name));',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('LINQ', 'List<int> numbers = new List<int> { 2, 3, 4, 5 };\nvar squaredNumbers = numbers.Select(x => x * x).ToList();',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Async/Await', 'public async Task<string> GetWebContentAsync(string url) {\n using (HttpClient client = new HttpClient())\n {\n string content = await client.GetStringAsync(url);\n return content;\n }\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
            """INSERT INTO snippets (title, code, language_id, category_id) VALUES('Attributes', '[Serializable]\nclass MySerializableClass {\n // Class implementation\n}',(SELECT id FROM languages WHERE name = 'C#'), (SELECT id FROM categories WHERE name = 'General'));""",
        ]
}

