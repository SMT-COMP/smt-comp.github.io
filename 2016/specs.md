## Machine Specifications

<p>
The competition will run on
the <a href="http://www.starexec.org">StarExec</a> cluster of machines
at the
<a href="http://www.uiowa.edu/">University of Iowa</a>.
</p>

<p>
The machines have these specifications:
</p>

<pre>
# Starexec stats nodes 0 - 32:
Intel(R) Xeon(R) CPU E5-2609 0 @ 2.40GHz (2393 MHZ)
    10240  KB Cache
    129022 MB main memory

# Starexec stats nodes 33 - 192:
Intel(R) Xeon(R) CPU E5-2609 0 @ 2.40GHz (2393 MHZ)
    10240  KB Cache
    258294 MB main memory

# Software:
OS:     Red Hat Enterprise Linux Server release 7.2 (Maipo)
kernel: 3.10.0-327.10.1.el7.x86_64
glibc:  gcc-4.8.5-4.el7.x86_64
        glibc-2.17-106.el7_2.4.i686
</pre>

<p>
A StarExec virtual machine image is available
<a href="https://www.starexec.org/vmimage/">here</a>.
</p>

<p>
The machines have 2 processors each and 4 cores per processor.  For
the competition, two job-pairs will be run on a given machine at a
given time (one on each processor, with 4 cores available), and the
available memory will be capped at 61440&nbsp;MB.
</p>

<p>
<b>We reserve the right to make software and configuration changes
before the competition.  Please exercise your solver(s) on a few
benchmarks to ensure that they run successfully!</b>
</p>
