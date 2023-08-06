from generate_docs.markdown import MarkdownPage, build_doc_link, verify_link, build_req_link
from generate_docs.repo import Repo, LanguageCollection


def _get_intro_text(language: LanguageCollection) -> str:
    introduction = f"Welcome to Sample Programs in {language.get_readable_name()}!"
    docs = f"""To find documentation related to the {language.get_readable_name()} 
code in this repo, look [here]({language.sample_program_url})."""
    if not verify_link(language.sample_program_url):
        return introduction
    else:
        return " ".join([introduction, docs])


def _get_sample_programs_text() -> str:
    return """Below, you'll find a list of code snippets in this collection.
Code snippets preceded by :warning: link to a GitHub 
issue query featuring a possible article request issue. If an article request issue 
doesn't exist, we encourage you to create one. Meanwhile, code snippets preceded 
by :white_check_mark: link to an existing article which provides further documentation."""


def _generate_program_list(language: LanguageCollection) -> list:
    """
    A helper function which generates a list of programs for the README.
    :param language: a language collection
    :return: a list of sample programs list items
    """
    list_items = list()
    for program in language.sample_programs:
        readable_name = program.normalized_name.replace("-", " ").title()
        doc_link = build_doc_link(program, f"{readable_name} in {language.get_readable_name()}")
        req_link = build_req_link(program)
        list_items.append(f"- {doc_link} [{req_link}]")
    return list_items


def _generate_testing_section(language: LanguageCollection):
    test_data = language.get_test_data()
    if not test_data:
        return """This language currently does not feature testing. If you'd like to help in the efforts to test all
of the code in this repo, consider creating a testinfo.yml file with the following information:
        
```yml
folder:
  extension: 
  naming:

container:
  image: 
  tag: 
  cmd:
```

See the [Glotter project](https://github.com/auroq/glotter) for more information on how to create a testinfo file. 
"""
    else:
        return f"""The following list shares details about what we're using to test all Sample Programs in 
{language.get_readable_name()}.
        
- Docker Image: {test_data["container"]["image"]}
- Docker Tag: {test_data["container"]["tag"]}

See the [Glotter project](https://github.com/auroq/glotter) for more information on how we handle testing. 
"""


def _generate_credit():
    return """---
This page was generated automatically by the Sample Programs Docs Generator. 
Find out how to support this project [here](https://github.com/TheRenegadeCoder/sample-programs-docs-generator)."""


class ReadMeCatalog:
    """
    An representation of the collection of READMEs in the Sample Programs repo.
    """

    def __init__(self, repo: Repo):
        """
        Constructs an instance of a ReadMeCatalog.
        :param repo: a repository instance
        """
        self.repo: Repo = repo
        self.pages: dict[str, MarkdownPage] = dict()
        self._build_readmes()

    def _build_readme(self, language: LanguageCollection) -> None:
        """
        Creates a README page from a language collection.
        :param language: a programming language collection (e.g., Python)
        :return: None
        """
        page = MarkdownPage("README")

        # Introduction
        page.add_content(f"# Sample Programs in {language.get_readable_name()}")
        page.add_section_break()
        page.add_content(_get_intro_text(language))
        page.add_section_break()

        # Sample Programs List
        page.add_content("## Sample Programs List")
        page.add_section_break()
        page.add_content(_get_sample_programs_text())
        page.add_section_break()
        page.add_content(*_generate_program_list(language))
        page.add_section_break()

        # Testing
        page.add_content("## Testing")
        page.add_content(_generate_testing_section(language))
        page.add_content(_generate_credit())

        self.pages[language.name] = page

    def _build_readmes(self) -> None:
        """
        Generates all READMEs for the repo.
        :return: None
        """
        for language in self.repo.languages:
            self._build_readme(language)
