% ----- Vertical layout with Four Corner Notation
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fcvertical}
\LoadClass[12pt,landscape,a5paper,twoside]{article}
%
% ----- Packages
\RequirePackage[landscape]{geometry}
\RequirePackage{fontspec}
\RequirePackage{xeCJK}
\RequirePackage{fancyhdr}
\RequirePackage{graphicx}
%
% ----- Fonts
%% ---- East Asian characters
\setCJKmainfont[Vertical=RotatedGlyphs,RawFeature={vertical:+vrt2}]{I.MingCP-Regular}%
\setCJKfamilyfont{bpmffont}[Vertical=RotatedGlyphs,RawFeature={vertical}]{I.MingCP-Regular}
\newcommand*{\txtfc}[1]{{\CJKfamily{bpmffont}#1}}
%
% ----- geometry
\geometry{
  a5paper,
  left=1in,
  right=1in,
  top=2.88em,
  bottom=2.88em,
  bindingoffset=0mm,
  headheight=15pt,
  headsep=0pt,
  footskip=15pt,
}
%
% ----- page style
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[RO]{\makebox[-.5in][c]{\hspace{.5pt}\rotatebox{90}{\thepage}}}%
\fancyhead[RE]{\makebox[-.5in][c]{\hspace{.5pt}\rotatebox{90}{\thepage}}}%
\endinput