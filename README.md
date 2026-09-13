<section style="max-width:700px; margin:auto; font-family:Arial, sans-serif; line-height:1.7; color:#333;">
  <h1 style="text-align:center; color:#2c3e50;">Django Clothing Store</h1>
  

  <p align="center">
  <img src="./doc/clothing-store.png" width="700"/>
  </p>
</section>

<h2>About</h2>
<p>A clothing store website built with Django.
  In this project, you can choose shirts based on color and size.</p>


<h2>Features</h2>
<ul>
  <li>Session Authentication</li>
  <li>Iranian Phone Number Validation</li>
  <li>Role-Based Permissions</li>
  <li>Admin & Customer Dashboards</li>
  <li>Product Variants (Color & Size)</li>
  <li>Product Filtering</li>
  <li>Product Ordering</li>
  <li>Product Searching</li>
  <li>Product Rating</li>
  <li>Product Commenting</li>
  <li>Shopping Cart</li>
  <li>Coupon System</li>
  <li>Order Management</li>
  <li>Payment Integration</li>
</ul>


<h2>Technologies</h2>
<ul>
  <li> Python</li>
  <li> Django</li>
  <li> PostgreSQL</li>
  <li> Google OAuth</li>
  <li> HTML, CSS, JavaScript</li>
</ul>


<h2>⚙️ Installation (Windows)</h2>

<p>Follow these steps to set up and run the project locally.</p>

<hr>

<h3>1. Clone the repository</h3>

```bash
git clone https://github.com/mhmdheydarii/Clothing-Store-Website.git
```

<br>

<h3>2. Navigate to the project directory</h3>

```bash
cd Clothing-Store-Website
```

<br>

<h3>3. Create a virtual environment</h3>

```bash
python -m venv .venv
```

<br>

<h3>4. Activate the virtual environment</h3>

<p><b>CMD</b></p>

```cmd
.venv\Scripts\activate
```

<p><b>PowerShell</b></p>

```powershell
.\.venv\Scripts\Activate.ps1
```

<p>
After activation, you should see something similar to:
</p>

```bash
(.venv)
```

<p>
at the beginning of your terminal line.
</p>

<br>

<h3>5. Install dependencies</h3>

<p>If the project includes a <code>requirements.txt</code> file:</p>

```bash
pip install -r requirements.txt
```

<br>

<h3>6. Configure environment variables</h3>

<p>Create a .env file in the project root and add the required environment variables.</p>

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS = "*"

NAME=db-name
USER=db-user
PASSWORD-db-password
HOST=db-hose

EMAIL_USER=your email address
EMAIL_PASSWORD=your email password
```
<br>

<h3>7. Run the project</h3>


```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```

<hr>

<details>
<summary><b>❌ Deactivate Virtual Environment</b></summary>

<br>

To exit the virtual environment:

```bash
deactivate
```

</details>

<br>

<p align="center">
⭐ If you found this project useful, consider giving it a star.
</p>
