# i3a

i3a is a set of scripts used for automation of i3 and sway window manager
layouts.

## Automation list

### i3a-master-stack

Provides automatic master-stack layout, which is known from e.g. DWM. The
following kinds of the layout are possible:

- master-stack area with DWM-like stack (stack windows are split)
- master-stack area with i3-like stack (stack windows are actual stack)

### i3a-swap

Swap master and stack areas from i3a-master-stack (technically it doesn't
require running i3-master-stack).

### i3-swallow

Provides automatic "swallowing": when a program runs a child process, the
parent is automatically hidden (moved to the scratchpad), which looks like if
it was replaced, or "swallowed" by the child window. It is especially useful
for graphical programs (video player, document viewer etc.) run from the
terminal.

Provides a means of filtering both parent programs which can be swallowed and
child programs which can trigger swallowing.

### i3a-move-to-empty

Moves currently focused container to the first empty workspace. Keep in mind
that this script relies on numbering of the workspaces.
