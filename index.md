## SMT-COMP 2019

### Introduction

#### Decision procedures.
Decision procedures for Satisfiability Modulo Theories (SMT) are of
continuing interest for many verification applications. SMT solvers are
typically used for verification as backends: a verification problem or
subproblem is translated into an SMT formula and submitted to the SMT
solver. The solver then attempts to report satisfiability or
unsatisfiability of the formula. The advantage SMT solvers are usually
considered to have over pure SAT solvers, which are also often used as
verification backends (e.g., for bounded model checking), is the higher
level of abstraction at which they can operate.  By implementing
theories like arithmetic, arrays, and uninterpreted functions directly,
SMT solvers have the promise to provide higher performance than SAT
solvers working on encodings of such structures to the bit level.

#### Standard formats.
The additional promise of SMT over pure SAT is balanced by additional
challenges. Since SMT deals with first-order (most commonly
quantifier-free) formulas instead of purely propositional ones, creation
and widespread adoption of a common input language is more difficult
than for SAT. It is furthermore more important, since the more
expressive setting of SMT potentially allows more room for variation in
the exact details of the logic (e.g., sorted or unsorted, total or
partial functions, etc.). Hence, translations between input formats of
different tools are more complex, and in some cases it may even not be
clear what such a translation should be. This makes the issue of input
format critical. For combination with other tools like skeptical proof
assistants (requiring a proof of every theorem validated by an external
tool), common output formats for objects like proofs and models are also
necessary for the adoption of SMT.

#### Competition.
 The Satisfiability Modulo Theories Competition (SMT-COMP) arose from
the SMT-LIB (Satisfiability Modulo Theories Library) initiative to spur
adoption of the common, community-designed SMT-LIB formats, and to spark
further advances in SMT, especially for verification. Competitions in
other automated reasoning fields, such as CASC and the SAT competition,
have helped inspire continuing improvements in tools from year to year.
The first SMT-COMP was held in 2005 as a satellite event of the 17th
International Conference on Computer-Aided Verification (CAV). The
experience with SMT-COMP 2005 confirmed the community's expectations
that a public competition would indeed motivate implementors of SMT
solvers to adopt the common SMT-LIB input format. Subsequent SMT-COMPs
have provided further evidence that such a competition can stimulate
improvement in solver implementations: solvers entered in each
competition have improved significantly over those in previous
competitions.

You can use the [editor on GitHub](https://github.com/SMT-COMP/smt-comp.github.io/edit/master/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/SMT-COMP/smt-comp.github.io/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
