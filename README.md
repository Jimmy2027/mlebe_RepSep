# An Optimized Registration Workflow and Standard Geometric Space for Small Animal Brain Imaging

These are the content files used to generate scientific communication materials for the project originally titled “Improving Registration in Small Animal Brain Imaging”.

## Dependencies

A full list of unabmiguously identified dependency constraints is specified [here](.gentoo/sci-publications/irsabi/irsabi-99999.ebuild) (following the [Package Manager Specification format](https://dev.gentoo.org/~ulm/pms/head/pms.html#x1-690008.2)). 
On a Gentoo Linux system, dependencies can be automatically managed with the included install script:

```
su -
cd /path/to/irsabi
cd .gentoo
./install.sh
```

## Compilation Instructions

This is a [RepSeP](https://github.com/TheChymera/RepSeP)-style document.
The data processing step is run asynchronously from the document compilation, and is triggered via the `prepare/run.sh` script.
The data processing by default takes place in `~/data_scratch`, which we suggest can be created as a symlink to a volume which has more space:

```
mkdir /mnt/largevolume/data_scratch
ln -s /mnt/largevolume/data_scratch ~/data_scratch
```
