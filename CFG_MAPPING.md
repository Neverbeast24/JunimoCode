# JunimoCode CFG → Implementation Map

This document maps *grammar-level constructs* (CFG “nonterminals”) to the functions that parse them in the two pipelines:

- Syntax-only pipeline: `parser_syntax.py`
- Semantic/runtime pipeline: `semantic.py`

> Note: The project uses two separate recursive-descent parsers with partially duplicated logic. Any CFG alignment work must usually be applied to both.

## Program structure

- **<program> / start-end framing** (`planting$ … perfection$`)
  - Syntax: `Parser.parse()` in `parser_syntax.py` (starts around line 1671)
  - Semantic: `Parser.parse()` in `semantic.py` (starts around line 2416)

- **<global_decl> (farmhouse crop declarations)**
  - Syntax: handled inside `Parser.parse()` when seeing `FARMHOUSE` in `parser_syntax.py`
  - Semantic: handled inside `Parser.parse()` when seeing `FARMHOUSE` in `semantic.py`

- **<craft_def> (function definition)**
  - Syntax: `Parser.init_craft()` in `parser_syntax.py` (around line 2965)
  - Semantic: craft-handling block inside `Parser.parse()` in `semantic.py` (around line 2510+)

- **<pelican_def> (main function)**
  - Syntax: `Parser.pelican()` in `parser_syntax.py` (around line 1820+)
  - Semantic: pelican-handling block inside `Parser.parse()` in `semantic.py` (around line 2580+)

## Statement lists

- **<stmt_list> / <body>**
  - Syntax: `Parser.body()` in `parser_syntax.py` (starts around line 1908)
  - Semantic: `Parser.body()` in `semantic.py` (starts around line 2710)

- **<stmt> dispatch (“what statements are allowed here?”)**
  - Syntax: `Parser.is_statement()` in `parser_syntax.py` (around line 2348)
  - Semantic: `Parser.is_statement()` in `semantic.py` (around line 3210)

## Declarations & assignments

- **<crop_decl>** (`crop Identifier …`)
  - Syntax: `Parser.crop_dec()` in `parser_syntax.py` (around line 2396)
  - Semantic: `Parser.crop_dec()` in `semantic.py` (around line 3053)

- **<assignment> / <compound_assignment>** (`=`, `+=`, `-=`, `*=`, `/=`)
  - Syntax: handled in `Parser.body()` via `Parser.init_crop()` / `Parser.assign_val*()` in `parser_syntax.py`
  - Semantic: handled in `Parser.body()` via `Parser.crop_init()` + expression parsing in `semantic.py` (crop init starts around line 3146)

- **<unary_stmt>** (`++A`, `A++`, `--A`, `A--`)
  - Syntax: handled in `Parser.body()` in `parser_syntax.py`
  - Semantic: handled in `Parser.body()` in `semantic.py`

## Control flow

- **<fall_stmt> (for loop)**
  - Syntax: `Parser.fall_stmt()` in `parser_syntax.py` (around line 3259)
  - Semantic: `Parser.fall_stmt()` in `semantic.py` (around line 3217)

- **<winter_stmt> (while loop)**
  - Syntax: handled in `Parser.body()` + `Parser.star_winter_condition()` in `parser_syntax.py` (condition helper around line 3817)
  - Semantic: `Parser.winter_stmt()` in `semantic.py` (around line 3397)

- **<star_stmt> / <dew_stmt> (if / else)**
  - Syntax: `Parser.star_stmt()` and `Parser.dew_stmt()` in `parser_syntax.py` (around lines 3635 and 3789)
  - Semantic: `Parser.star_expr()` in `semantic.py` (around line 3308)

- **<break_stmt> / <next_stmt>**
  - Syntax: handled in `Parser.body()` in `parser_syntax.py` with scope flags (`in_loop`, `in_condition`)
  - Semantic: handled in `Parser.body()` in `semantic.py`

## I/O and calls

- **<collect_stmt>**
  - Syntax: `Parser.collect_stmt()` (called from `Parser.body()` in `parser_syntax.py`)
  - Semantic: handled in `Parser.body()` (creates `CollectNode`) in `semantic.py`

- **<ship_stmt>**
  - Syntax: `Parser.ship_stmt()` (called from `Parser.body()` in `parser_syntax.py`)
  - Semantic: handled in `Parser.body()` (creates `ShipNode`) in `semantic.py`

- **<craft_call>** (`Identifier( … )`)
  - Syntax: `Parser.call_craft()` in `parser_syntax.py` (around line 3165)
  - Semantic: handled in `Parser.body()` by building `CraftCallNode` in `semantic.py`

## Expressions & conditions

- **<expr> (addition/subtraction)**
  - Syntax: `Parser.expr()` in `parser_syntax.py` (around line 4134)
  - Semantic: `Parser.expr()` in `semantic.py` (around line 3641)

- **<term> (mul/div/mod)**
  - Syntax: `Parser.term()` in `parser_syntax.py` (around line 4117)
  - Semantic: `Parser.term()` in `semantic.py` (around line 3624)

- **<factor> (atoms, unary ! and - , parentheses, literals, identifiers)**
  - Syntax: `Parser.factor()` in `parser_syntax.py` (around line 4083)
  - Semantic: `Parser.factor()` in `semantic.py` (around line 3475)

- **<condition> / comparisons / logical ops**
  - Syntax: split across `Parser.star_winter_condition()` + expression helpers in `parser_syntax.py`
  - Semantic: `Parser.own_if_expr()` + `Parser.comp_expr()` + arithmetic parsing in `semantic.py` (around lines 3427–3470)

## Harvest (return)

- **<harvest_stmt>** (`harvest <expr>$`)
  - Syntax: handled in `Parser.body()` in `parser_syntax.py` (around line 2291)
  - Semantic: handled in `Parser.body()` in `semantic.py` (around line 3003)

Enforced constraints (both pipelines):
- `harvest` is **not allowed** in `pelican()`.
- `harvest` is **only allowed** inside `craft`.
- After a `harvest` appears in a craft, **no further statements** are allowed (only closing braces/newlines/comments).
