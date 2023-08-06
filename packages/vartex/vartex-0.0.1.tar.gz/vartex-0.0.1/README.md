# VarTex
VarTeX is a command line tool that allows you to generate and compile 
multiple LaTeX files from a single template file and a JSON/CSV file containing the variables.

### Usage

---
To run the command, use the following command:

```bash
vartex tex_filename <flag> variable_filename 
```

For example, in the `example` directory, to use the JSON file `variables.json` to generate the LaTeX file `template.tex`:

```bash
vartex example/cover_letter.tex --json variables.json
```