================================================
input: automatise commands using external inputs
================================================

``input`` is a way to use external data (like file in a specific format) as input
arguments. It may be seen as a something similar to ``--output`` but for inputs.


csv
===

CSV (for Comma-Separated Values) is a common format for tabular data. It is widely used in
spreadsheet software (at least at en export format). With ``csv`` command, you can use
columns a CSV file as arguments to li commands.

To set the command, you'll write in sequence what to do with each column of your data.
For each column you can:

- specify a short option name using ``-s ARGUMENTS, --short ARGUMENTS`` (short options are
  the ones with a single ``-``)
- specify a long option name using ``-l ARGUMENTS, --long ARGUMENTS`` (long options are
  the ones with two ``-``)
- specify a positional argument using ``-p ARGUMENTS, --positional ARGUMENTS``
- indicate to use the column data with ``stdin`` using ``-i, --stdin``
- ignore the column if it's not used in the li command, using ``-x, --ignore``

After each column specification, you may use a filter to manage the value. So far the
following filters are available:

``-S, --split``
  This will split the value (on any whitespace character, discarding empty values) and
  repeat the option which each item. This is useful when you are using an option which can
  be repeated (like ``-t TAG, --tag TAG`` with ``li blog set``).

``-E ARGUMENTS, --empty ARGUMENTS``
  Indicate what to do if the column value is empty (by default en empty string is used).
  You can use either ``skip`` to skip the whole row, or ``ignore`` so the option will not
  be set at all (which is different from the default which will still set the option but
  with an empty string).

CSV file is read from stdin, and by default unicode is expected. You may force an encoding
by using ``--encoding ENCODING``.

By default all the rows are read, but you may want to ignore first rows (if they are used
for columns title, or if you have already handled part of the list). To do that, use the
``-r ROW, --row ROW`` option.

When you test your command, it is better to do a dry run to see what will happen. The
``-D, --debug`` option is here for that: if you set it, the commands won't be actually
run, but the exact command which would be executed will be printed on screen. You should
always use this option first until you're sure that what you want will be executed.

You may add verbosity level to help debugging. With a verbosity level of 2 (i.e. ``-vv``)
the value read from CSV will be printed.

By default stdout and stderr of each launched command is ignored, but you can log them to
files using respectively ``--log LOG`` and ``--log-err LOG_ERR`` where ``LOG`` and
``LOG_ERR`` are paths to a log file to create.

Once all the sequence and options are set, you write the li command that you want to use,
with all the needed static option (i.e. options which must be used each time).


example
-------

Louise as a spreadsheet with a table like this:

============================  ============  =============  ===============
title                         body          internal data  tags
============================  ============  =============  ===============
Some title                    a body        ABC            li demo
Something else                another body  XYZ            li demo
Third one                     third body    VWZ            special_tag li
This one doesn't have a body                123            li demo numbers
last one                      last body     456            li demo numbers
============================  ============  =============  ===============

She wants to use it as input data to create blog posts.

She first saves the file using CSV format, let's say to ``~/blog_input.csv``.

Then she checks ``li blog set --help`` to get name of options to use. She'll need to use
``--title`` for title, ``stdin`` for the body and ``-t`` for tags. Louise wants to
activate comments, so she also wants to use ``-C`` for all posts, and a tag to says it's
coming from the spreadsheet (using ``-t spreadsheet``) .

The first row of the table is used for columns headers, so she'll start at row 1 with ``-r
1``.

There is one row without body, Louise want to skip any row without body so she'll use the
``-E skip`` filter, just after specifying the body row.

Reading column by column, the sequence is like this:

``-l title``
  a title which goes to the ``--title`` long option of ``li blog``
``-i -E skip``
  a body which goes to the stdin of ``li blog``. If the body is empty, the ``-E skip``
  filter tells to skip the whole row.
``-x``
  the ``internal data`` column is not used, so it is ignored
``-s t -S``
  the last column are the tags, so the ``-t`` short option is used. There are several of
  them separated by spaces, so the ``-S`` filter is used to split the values.

First she'll use the ``-D, --debug`` to check that the commands which will be executed are
the expected one::

  $ li input csv -D -r 1 -l title -i -E skip -x -s t -S blog set -C -t spreadsheet < ~/blog_input.csv

Everything seems fine, so she'll actually launch the command by running the same command
line but without the ``-D`` option::

  $ li input csv -r 1 -l title -i -E skip -x -s t -S blog set -C -t spreadsheet < ~/blog_input.csv

She could also have used ``--log`` and ``--log-err`` to check the logs of each command::

  $ li input csv -r 1 -l title -i -E skip -x -s t -S --log /tmp/jp_blog_stdout.log --log-err /tmp/jp_blog_stderr.log blog set -C -t spreadsheet < ~/blog_input.csv
