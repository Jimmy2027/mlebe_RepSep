# Improving Registration in Small Animal Brain Imaging

These are the content files used to generate scientific communication materials for the “Improving Registration in Small Animal Brain Imaging” project.

## Compilation Instructions

This is a [RepSeP](https://github.com/TheChymera/RepSeP)-based document.
As such, it is compiled by overwriting the RepSeP base system with the specific content files from this repository, and subsequently initiating a compound compilation command.
Satisfying the dependency requirements of RepSeP is mandatory for the compilation to succeed.
From your terminal, run the following commands line by line:

```sh
git clone git@github.com:TheChymera/RepSeP.git
git clone git@bitbucket.org:TheChymera/irsabi.git && cd irsabi
cp -rf ../RepSeP/pythontex .
```

If the above should fail with a `Permission denied (publickey)` error, you should do one of the following:

* [Add an SSH key](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) to your GitHub account.
* Pull via the HTTPS links: `https://github.com/TheChymera/RepSeP.git` and `https://TheChymera@bitbucket.org/TheChymera/irsabi.git`, respectively.

### Poster

```sh
pdflatex -shell-escape article.tex && pythontex.py article.tex && pdflatex -shell-escape article.tex && bibtex article && pdflatex -shell-escape article.tex && pdflatex -shell-escape article.tex
```

## Contributing

If you wish to contribute to this repository please make sure never to run `git add .` - or any other Git command which would include any RepSeP file sharing this document's root directory to the document's Git history.
The only files which should be tracked are those which inevitably diverge from the upstream RepSeP example, due to the document contents.
