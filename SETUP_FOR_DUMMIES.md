# Setup for Dummies  
*(Yes, This Is the “I Just Want It to Work” Guide.)*

If you found this project via Reddit and just want to **convert an Earth date to a stardate**
without learning how Python, terminals, or computers *really* work — this file is for you.

If you already know what you’re doing:
- you can skim this
- or ignore it entirely
- nothing here will surprise you

This guide assumes **Windows** and a **normal amount of patience**
*(and no, I will never write a version for Mac. Fuck that bullshit!)*

---

## Step 0: What You’re Actually Doing

You are going to:

1. Install Python  
2. Make sure **pip** exists (Python’s package installer)
3. Download this project
4. Open *some kind* of terminal (PowerShell or Command Prompt, both fine)
5. Run two commands
6. Get a stardate

That’s it. You are not signing up for a lifestyle change.

---

## Step 1: Install Python (One Time Only)

If you already have Python **3.9 or newer**, you can skip this section.

Otherwise:

1. Go to  
   👉 https://www.python.org/downloads/windows/

2. Click **Download Python 3.x**

3. Run the installer

4. **IMPORTANT — DO NOT SKIP THIS:**  
   On the first screen, check the box that says:

   ☑ **Add Python to PATH**

5. Click **Install Now**

If you miss that checkbox, things later will not work and will not explain why.

---

## Step 2: Make Sure `pip` Is Installed  
*(Do This Before Any Other Commands)*

`pip` is the tool Python uses to install extra packages.
This project will not run correctly without it.

### Check if pip exists

Open **PowerShell or Command Prompt**, then type:

```text
python -m pip --version
````

If you see something like:

```text
pip 25.x from ... (python 3.x)
```

✔ pip is installed — you can move on.

---

### If That Command FAILS

Run this instead:

```text
python -m ensurepip --upgrade
```

Then check again:

```text
python -m pip --version
```

If it still fails:

* Python was not installed correctly
* Reinstall Python and **make sure “Add Python to PATH” is checked**

Do not skip this step. Everything else depends on it.

---

## Step 3: Download This Project

1. Click the green **Code** button on GitHub
2. Choose **Download ZIP**

Your browser will almost certainly put this in your **Downloads** folder.

The folder will be called something like:

```
kelvin-stardate-main
```

(or similar)

---

## Step 4: Extract the Files (Two Options)

You need the files **out of the ZIP** and **not trapped in Downloads forever**.

### Option A: File Explorer (Recommended)

1. Open **File Explorer**
2. Go to **Downloads**
3. Right-click the ZIP file
4. Click **Extract All**
5. Click **Extract**

You’ll get a normal folder.

Now:

* drag that folder somewhere sensible
  (Desktop is fine, Documents is fine, inside another folder is fine. So long as you don't leave it in downloads!)

You are done with extraction.

---

### Option B: Command Line (If You Prefer)

If you already know how to unzip files from the command line,
you do not need instructions here.

---

## Step 5: Open a Terminal (PowerShell *or* Command Prompt)

This project works in **both PowerShell and Command Prompt**.

Windows sometimes:

* opens PowerShell that launches Command Prompt
* opens Command Prompt that launches PowerShell
* does something else entirely

That is fine. We are not fixing Windows today. Do that on your own time.

To open *something* usable:

1. Press the **Windows key**
2. Type:

   * `powershell` **or**
   * `cmd`
3. Press **Enter**

If text appears and you can type, you’re good.

---

## Step 6: Go to the Project Folder

In the terminal, move into the folder you extracted.

If you put it on your Desktop:

```text
cd Desktop\kelvin-stardate
```

To confirm you’re in the right place:

```text
dir
```

You should see files like:

* `kelvin_stardate_cli.py`
* `requirements.txt`

If you don’t, you’re in the wrong folder.

---

## Step 7: Install the Required Packages

Now that `pip` definitely exists, run:

```text
python -m pip install -r requirements.txt
```

This installs:

* terminal color support
* testing tools
* a future configuration library

It may print a lot of text. That is normal.

---

## Step 8: Run the Converter

Finally:

```text
python kelvin_stardate_cli.py
```

You should see a menu.

If you do:
✔ congratulations, you’re done!

---

## Common Problems (And What They Mean)

### “python is not recognized”

* Python was not added to PATH
* Reinstall Python and **check the box**

### `pip` errors

* pip was not installed
* Run `python -m ensurepip --upgrade`

### PowerShell opens when I expected Command Prompt (or vice versa)

* This is Windows being Windows
* As long as commands run, it does not matter

---

## If You Actually Know What You’re Doing

You can:

* use PowerShell or cmd
* use virtual environments
* install dependencies however you like
* skip half this file

This guide is not trying to stop you.

---

## Final Notes

* You cannot break your computer with this
* You are allowed to use tools without mastering the tooling
* If you get stuck, copy the error message *exactly* when asking for help

This file exists because not everyone needs to become a developer
just to get a stardate.
