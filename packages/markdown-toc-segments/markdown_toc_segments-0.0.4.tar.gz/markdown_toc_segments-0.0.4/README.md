# markdown-toc-segments

![Github CI](https://github.com/justmars/markdown-toc-segments/actions/workflows/main.yml/badge.svg)

## Purpose

Most structured cases in Philippine jurisprudence follow a certain format that can be dissected through an outline. See [sample file](./temp.md). Assuming a proper table of contents can be generated from the markdown file, can create segments from the full text:

```py
>>> from pathlib import Path
>>> from markdown_toc_segments import Outline
>>> f = Path().cwd() / "temp.md"
>>> obj = Outline(raw=f.read_text())
>>> obj.footnotes
[Footnote(id='fn:1', markup='I am no footnote\xa0↩'),
 Footnote(id='fn:2', markup='One does not simply footnote\xa0↩'),
 Footnote(id='fn:3', markup='A red day ere the sun foonotes\xa0↩'),
 Footnote(id='fn:4', markup='The lord of the footnotes\xa0↩'),
 Footnote(id='fn:5', markup='Footnotes is the precious\xa0↩')]
 >>> obj.segments
 [Segment(id='ponencia', markup='<p>This is a sample decision written in markdown to illustrate the ability to compartamentalize text.<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>'),
 Segment(id='antecedents', markup='<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit,<sup id="fnref:2"><a class="footnote-ref" href="#fn:2">2</a></sup> sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat<sup id="fnref:3"><a class="footnote-ref" href="#fn:3">3</a></sup> nulla pariatur. Excepteur sint occaecat cupidatat non proident,<sup id="fnref:4"><a class="footnote-ref" href="#fn:4">4</a></sup> sunt in culpa qui officia deserunt mollit anim id est laborum.</p>'),
 Segment(id='version-of-the-defense', markup='<p>XXX</p>'),
...
 Segment(id='the-courts-ruling', markup='<p>The Court dismisses the appeal.</p>'),
 Segment(id='this-is-a-proper-headline', markup='<p>XXXX</p>'),
...]
>>> obj.tree
[
  Item(
    id='ponencia',
    label='Ponencia',
    segment=Segment(id='ponencia', markup='<p>This is a sample decision written in markdown to illustrate the ability to compartamentalize text.<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>'),
    text='This is a sample decision written in markdown to illustrate the ability to compartamentalize text.%% I am no footnote %%',
    children=[
      Item(
        id='antecedents',
        label='Antecedents',
        segment=Segment(id='antecedents', markup='<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit,<sup id="fnref:2"><a class="footnote-ref" href="#fn:2">2</a></sup> sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat<sup id="fnref:3"><a class="footnote-ref" href="#fn:3">3</a></sup> nulla pariatur. Excepteur sint occaecat cupidatat non proident,<sup id="fnref:4"><a class="footnote-ref" href="#fn:4">4</a></sup> sunt in culpa qui officia deserunt mollit anim id est laborum.</p>'), text='Lorem ipsum dolor sit amet, consectetur adipiscing elit,%% One does not simply footnote %% sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat%% A red day ere the sun foonotes %% nulla pariatur. Excepteur sint occaecat cupidatat non proident,%% The lord of the footnotes %% sunt in culpa qui officia deserunt mollit anim id est laborum.', children=[
          Item(
            id='version-of-the-defense',
            label='Version of the Defense',
            segment=Segment(id='version-of-the-defense',
            markup='<p>sffffffffm dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Adipiscing diam donec adipiscing tristique risus nec feugiat in fermentum. Porttitor eget dolor morbi non. In arcu cursus euismod quis viverra nibh. Nec ultrices dui sapien eget mi proin sed. Ultrices eros in cursus turpis massa. Sit amet consectetur adipiscing elit. Quis ipsum suspendisse ultrices gravida. Vel elit scelerisque mauris pellentesque pulvinar pellentesque. At urna condimentum mattis pellentesque id nibh tortor. Amet tellus cras adipiscing enim eu turpis egestas. Non blandit massa enim nec dui nunc mattis. Viverra ipsum nunc aliquet bibendum enim facilisis gravida neque. Cras sed felis eget velit aliquet sagittis id consectetur. Donec pretium vulputate sapien nec sagittis aliquam malesuada. Orci eu lobortis elementum nibh tellus molestie nunc non. Risus sed vulputate odio ut enim blandit. Enim nulla aliquet porttitor lacus luctus accumsan tortor. Cursus euismod quis viverra nibh cras pulvinar mattis.</p>'), text='sffffffffm dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Adipiscing diam donec adipiscing tristique risus nec feugiat in fermentum. Porttitor eget dolor morbi non. In arcu cursus euismod quis viverra nibh. Nec ultrices dui sapien eget mi proin sed. Ultrices eros in cursus turpis massa. Sit amet consectetur adipiscing elit. Quis ipsum suspendisse ultrices gravida. Vel elit scelerisque mauris pellentesque pulvinar pellentesque. At urna condimentum mattis pellentesque id nibh tortor. Amet tellus cras adipiscing enim eu turpis egestas. Non blandit massa enim nec dui nunc mattis. Viverra ipsum nunc aliquet bibendum enim facilisis gravida neque. Cras sed felis eget velit aliquet sagittis id consectetur. Donec pretium vulputate sapien nec sagittis aliquam malesuada. Orci eu lobortis elementum nibh tellus molestie nunc non. Risus sed vulputate odio ut enim blandit. Enim nulla aliquet porttitor lacus luctus accumsan tortor. Cursus euismod quis viverra nibh cras pulvinar mattis.', children=[...])]
      )
    ]
  )
]
```
