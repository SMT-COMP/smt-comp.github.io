## Machine Specifications

The competition will run on the [StarExec](http://www.starexec.org/)
cluster of machines at the [University of Iowa](http://www.uiowa.edu/).

The machines have these specifications:

```markdown
Intel(R) Xeon(R) CPU E5-2609 0 @ 2.40GHz (2393 MHZ)
    10240  KB Cache
    129022 MB main memory

# Software:
OS:    Red Hat Enterprise Linux Server release 7.2 (Maipo)
kernel:    3.10.0-514.16.1.el7.x86_64
glibc:    gcc-4.8.5-4.el7.x86_64
          glibc-2.17-157.el7_3.1.i686
```

A StarExec virtual machine image is available
[here](https://www.starexec.org/vmimage/).

The machines have 2 processors each and 4 cores per processor. For the competition, two job-pairs will be run on a given machine at a given time (one on each processor, with 4 cores available), and the available memory will be capped at 61440 MB.

**We reserve the right to make software and configuration changes before the competition. Please exercise your solver(s) on a few benchmarks to ensure that they run successfully!**
