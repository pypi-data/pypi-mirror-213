# genheader

## Introduction

![showcase](https://user-images.githubusercontent.com/83401142/144825570-210f51ed-ddfc-4a14-b84a-10db1aac8563.gif)

Injects c function prototypes(BSD-style) into header.

## Usage

`genheader [-h] -I header.h [dir/ ... file.c]`

You need to have a .h file with

- A line comment containing: `@functions` or `@func`
- End with `#endif` or `@end`

### examples

```c
#ifndef HEAD_H
# define HEAD_H

//	===== @functions =====
#endif
```

```c
//	@func
//	@end
```
