# Setup for Dummies  
*(Yes, This Is the “I Just Want It to Work” Guide.)*

If you found this project via Reddit and just want to **convert an Earth date to a stardate**
without learning how Python, terminals, or computers *really* work — this file is for you.

If you already know what you’re doing:
- you can skim this
- or ignore it entirely
- nothing here will surprise you

This guide assumes **Windows** and a **normal amount of patience**.  
*(No, I am still not writing a Mac version. Fuck that bullshit! If you're really that devoted, install a VM)*

---

## Step 0: What You’re Actually Doing

You are going to:

1. Install Python  
2. Create a **virtual environment** (this is important, but not scary)
3. Download this project
4. Open *some kind* of terminal (PowerShell or Command Prompt, both fine)
5. Run a few commands
6. Get a stardate

That’s it. You are not signing up for a lifestyle change.

---

## Step 1: Install Python (One Time Only)

If you already have **Python 3.9 or newer**, you can skip this section.

Otherwise:

1. Go to  
   👉 https://www.python.org/downloads/windows/

2. Click **Download Python 3.x** (this should be the latest stable version)

3. Run the installer

4. **IMPORTANT — DO NOT SKIP THIS:**  
   On the first screen, check the box that says:

   ✅ **Add Python to PATH**
   
   This is safe for normal users and **required for the steps below**.
   If you already manage Python versions manually (pyenv, Conda, etc.), you already know when to ignore this.

5. Click **Install Now**

If you miss that checkbox, things later will not work and will not explain why.

---

## Step 2: Open a Terminal (PowerShell or Command Prompt)

This project works in **both PowerShell and Command Prompt**.

To open one:

1. Press the **Windows key**
2. Type:
   - `powershell` **or**
   - `cmd`
3. Press **Enter**

If text appears and you can type, you’re good.

---

## Step 3: Download This Project

1. Click the green **Code** button on GitHub
2. Choose **Download ZIP**

Your browser will probably put this in your **Downloads** folder.

The folder will be called something like:

```
kelvin-stardate-main
````

---

## Step 4: Extract the Files

You need the files **out of the ZIP** and **not trapped in Downloads forever**.

#### Recommended way:

1. Open **File Explorer**
2. Go to **Downloads**
3. Right-click the ZIP file
4. Click **Extract All**
5. Click **Extract**

You’ll get a normal folder.

Now drag that folder somewhere sensible:
- Desktop is fine
- Documents is fine
- Anywhere you can find again is fine

---

## Step 5: Go to the Project Folder

In the terminal, move into the folder you just extracted.

If you put it on your Desktop:

`cd Desktop\kelvin-stardate`

To confirm you’re in the right place:

`dir`

You should see files like:

* `pyproject.toml`
* `SETUP_FOR_DUMMIES.md` (aka, this file)
* `src\`

If you don’t, you’re in the wrong folder.

---

## Step 6: Create a Virtual Environment (Do Not Skip This)

A **virtual environment** is just a private sandbox for Python packages.
It prevents this project from messing with anything else on your computer.

You only need to do this **once per project**.

Run:

`python -m venv venv`

This creates a folder called `venv`.

Nothing scary has happened.

### Want to Know More? (Optional Reading)

If you’re curious what a virtual environment actually *is* or want more detail,
these are solid, beginner-friendly references:

- **Official Python documentation**  
  venv — Creation of virtual environments  
  https://docs.python.org/3/library/venv.html

- **Step-by-step walkthrough (GeeksforGeeks)**  
  How to Create a Python Virtual Environment  
  https://www.geeksforgeeks.org/python/create-virtual-environment-using-venv-python/

You do *not* need to read these to continue.
They exist so this file doesn’t have to explain everything itself.

---

## Step 7: Activate the Virtual Environment

#### PowerShell:

`venv\Scripts\Activate.ps1`

#### Command Prompt:

`venv\Scripts\activate`

After activation, your terminal prompt will change to include:

`(venv)`

If you see `(venv)` — good.
If you don’t — stop and fix this before continuing.

---

## Step 8: Make Sure `pip` Works (Quick Check)

Still inside `(venv)`, run:

`python -m pip --version`

If you see a version number, you’re fine.

If it fails:

`python -m ensurepip --upgrade`

Then try again.

---

## Step 9: Install the Project

This project uses modern Python packaging.
The easiest way is to install it **in editable mode**.

Run:

`pip install -e .`

This:

* installs required dependencies
* registers the `kelvin-stardate` command
* keeps the code editable if you update it later

Text will scroll. That’s normal.

---

## Step 10: Run the Converter

Now, simply run:

`kelvin-stardate`

You should see the interactive menu.

If you do:
✔ congratulations, you’re done!

---

## Common Problems (And What They Mean)

#### “python is not recognized”

* Python was not added to PATH
* Reinstall Python and **check the box**

#### `(venv)` does not appear

* The virtual environment is not activated
* Re-run the activate command for your terminal

#### `kelvin-stardate` is not recognized

* The project was not installed
* Make sure you ran `pip install -e .` **inside the venv**

---

## If You Actually Know What You’re Doing

You can:

* use Git instead of ZIP downloads
* manage environments however you like
* skip half this file

This guide is not trying to stop you.

---

## Final Notes

* You cannot break your computer with this
* Virtual environments are normal and safe
* You are allowed to use tools without mastering the tooling
* If you get stuck, copy the error message *exactly* when asking for help

This file exists because not everyone needs to become a developer
just to get a stardate.

---

### Why this ordering matters
- **venv comes before pip installs** (critical)
- users never install packages globally by accident
- matches your actual repo + CLI now
- future-you won’t have to explain “why didn’t you activate venv” ever again
