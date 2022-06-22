SMT-COMP Website Repository
---------------------------

This is the repository for the SMT-COMP website on GitHub Pages.

### How to create a page for a new edition of the competition

1. Add link color for year in `_includes/head.html`

2. Add navigation items for year to `_data/navigation.yml`

3. Copy `yyyy/index.md` into new subdirectory and update references to `yyyy`

4. Add track data to `_data/tracks.yml` (if updates required)

5. Add current competition to previous competitions in `_data/competitions.yml`
   and update `index.html` to point to new competition page

6. Create collections folders for years and add to `config.yml`
   - `_news_yyyy`
   - `_participants_yyyy`
   - `_results_yyyy`


### How to generate the website locally

 * `sudo gem install jekyll bundler jekyll-theme-dinky`
 * `jekyll build`
