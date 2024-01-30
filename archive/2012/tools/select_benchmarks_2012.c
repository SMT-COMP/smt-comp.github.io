/* select_benchmarks.c
 * Morgan Deters mdeters@cs.nyu.edu, 2007, 2008, 2009, and 2010.
 * For SMT-COMP 2010, updated from previous versions by the same author.
 * See smtcomp.org.
 *
 * UPDATED FOR SMT-COMP 2009:
 * The only difference from SMT-COMP 2008 and SMT-COMP 2009 is that
 * this version has been hacked to only include 100 QF_IDL benchmarks.
 *
 * UPDATED FOR SMT-COMP 2010:
 * + Commented out the SMT-COMP 2009 hack.
 * + Changed what a "family" is: now it's the top-level directory.  So
 *   in the "family" in the input file, everything after (and including)
 *   the first slash is ignored.
 * + In the input file, difficulties are now permitted to be a floating
 *   point number on the interval [0,5].
 * + Instead of easy/hard, we now do things on difficulty intervals
 *   [0,1], (1,2], (2,3], (3,4], and (4,5].
 *
 * NOTES ON THIS PROGRAM:
 *
 * This program reads a file that starts with a count N of records on a
 * line by itself, then N lines of the form:
 *
 *    division family category difficulty solution benchmarkid file
 *
 * The fields are delimited by a space.  benchmarkid is a nonnegative
 * integer; the rest (with the exception of difficulty) are strings with
 * no embedded spaces.  category is one of "check", "crafted", "industrial",
 * and "random".  "difficulty" is a double (in a format accepted by strtod())
 * in the range [0,5].  "solution" is one of "sat", "unsat", and "unknown".
 * "unknown" benchmarks are ineligible for selection; all others are eligible.
 * This program ignores the file field, and anything after (and including) the
 * first forward-slash in the family field.
 *
 * The input is expected to be grouped on fields, in left-to-right order.
 * That is, all benchmarks in a common division must be listed together;
 * all benchmarks in a common family and division must be listed together;
 * all such benchmarks with a common difficulty must be listed together;
 * and so on.
 *
 * On stdout, produce a list of distinct benchmarkids, one per line,
 * selected for SMT-COMP 2010.  The output is in no guaranteed order.
 * There is never any other output on stdout.  On stderr, produce
 * error messages (if any) or a list of statistics (if benchmark
 * selection is successful).  If there is a fatal error, the exit
 * status is nonzero; there may be a partial benchmarkid list on stdout
 * in such cases.  Only if the exit status is zero should the benchmarkid
 * list be used.
 *
 * This is the breakdown for selection:
 *
 *   1. All eligible benchmarks in category "check" are included.
 *
 *   2. For non-"check" benchmarks, division pools are created.  For each
 *      benchmark family, if the family has <= 200 eligible, non-"check"
 *      benchmarks, all are added to the division pool; otherwise,
 *      200 such benchmarks are added to the pool with the following
 *      distribution:
 *        20 with solution "sat"   and difficulty on the interval [0,1]
 *        20 with solution "sat"   and difficulty on the interval (1,2]
 *        20 with solution "sat"   and difficulty on the interval (2,3]
 *        20 with solution "sat"   and difficulty on the interval (3,4]
 *        20 with solution "sat"   and difficulty on the interval (4,5]
 *        20 with solution "unsat" and difficulty on the interval [0,1]
 *        20 with solution "unsat" and difficulty on the interval (1,2]
 *        20 with solution "unsat" and difficulty on the interval (2,3]
 *        20 with solution "unsat" and difficulty on the interval (3,4]
 *        20 with solution "unsat" and difficulty on the interval (4,5]
 *      If 20 are not available in one of these subdivisions, all available,
 *      eligible, non-"check" benchmarks that are available in the subdivision
 *      are included; to make 200, slots are reallocated to other subdivisions
 *      (for which sufficient benchmarks _are_ available) in equal amounts.
 *      Up to 9 slots can still remain unallocated; these are randomly
 *      reallocated to distinct subdivisions (for which sufficient benchmarks
 *      are available) so far as possible, or non-distinct subdivisions if
 *      sufficient benchmarks aren't available in some subdivisions.
 *
 *   3. For each division, N slots are allocated as follows (NOTE: for
 *      SMT-COMP 2010, N is expected to be 200 for all divisions):
 *        .85N from category "industrial"
 *        .10N from category "crafted"
 *        .05N from category "random"
 *      If there are fewer than .10N (resp. .05N) "crafted" or "random"
 *      benchmarks in the division pool, more "industrial" slots are
 *      allocated to make N total for the division.  If there are too few
 *      "industrial" benchmarks in the division pool, more "crafted" slots
 *      are allocated to make N total for the division.  As a last resort,
 *      "random" benchmarks can be allocated additional slots if there are
 *      no other benchmarks available in the pool.
 *
 *   4. For each category in each division, given that it has N slots
 *      allocated to it, the slot allocation is further subdivided as
 *      follows:
 *        floor(N/10) slots for solution "sat"   with difficulty on [0,1]
 *        floor(N/10) slots for solution "sat"   with difficulty on (1,2]
 *        floor(N/10) slots for solution "sat"   with difficulty on (2,3]
 *        floor(N/10) slots for solution "sat"   with difficulty on (3,4]
 *        floor(N/10) slots for solution "sat"   with difficulty on (4,5]
 *        floor(N/10) slots for solution "unsat" with difficulty on [0,1]
 *        floor(N/10) slots for solution "unsat" with difficulty on (1,2]
 *        floor(N/10) slots for solution "unsat" with difficulty on (2,3]
 *        floor(N/10) slots for solution "unsat" with difficulty on (3,4]
 *        floor(N/10) slots for solution "unsat" with difficulty on (4,5]
 *      If there aren't enough benchmarks in the pool meeting one or more of
 *      the above subdivided requirements for the category, the subdivision
 *      allocation is reduced to the number available in the pool that meet
 *      the requirements.  To make up the full category allotment,
 *      remaining slots are allocated equally to subdivisions with enough
 *      benchmarks in the pool meeting their requirements.  As above, up to
 *      9 slots can remain unallocated, and these are randomly allocated to
 *      distinct subdivisions, so far as possible, for which benchmarks are
 *      available in the pool meeting the necessary requirements; otherwise,
 *      they are randomly allocated to non-distinct subdivisions.
 *
 * In the end, N non-"check" benchmarkids per division are output,
 * together with all the "check" benchmarkids.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <math.h>

/* FAMILY_SIZE - the number of benchmarks to include in the division
 * pool from each family */
#define FAMILY_SIZE    200

/* number of non-check benchmarks to include in each division in output */
#define N 200

/* N_POOL_ENTRIES - used to size some arrays; must be at least as
 * large as the total number of eligible non-"check" benchmarks in the
 * largest division */
#define N_POOL_ENTRIES 50000

typedef enum category { INDUSTRIAL, CRAFTED, RANDOM, CHECK } category_t;
typedef enum solution { SAT, UNSAT, UNKNOWN } solution_t;

/* # slots available in division selection for each category */
#define CATEGORY_ALLOTMENT { 85*N/100, 10*N/100, 5*N/100 }

/* GCC required */
#define MIN(x,y) \
  ({ unsigned __x = (x); unsigned __y = (y); __x < __y ? __x : __y; })

/* family pool */
typedef struct fpool {
  unsigned n; /* total number that are in the pool */

  struct {
    /* count of benchmarks with given solution & difficulty */
    unsigned n[2][5]; /* [solution][difficulty_interval] */
  } solutiondiff;
} fpool_t;

/* division pool */
typedef struct dpool {
  unsigned alloc; /* total number that are in the pool */
  unsigned n; /* total number that are in the pool */

  struct {
    /* linked list of benchmarks with given category/solution/difficulty */
    unsigned first[3][2][5]; /* [category][solution][difficulty_interval] */

    /* benchmark count with given category/solution/difficulty */
    unsigned n[3][2][5];     /* [category][solution][difficulty_interval] */

    /* benchmark count with the given category */
    unsigned nc[3];          /* [category] */

    unsigned next[N_POOL_ENTRIES]; /* next ptr in linked list */
    category_t values[N_POOL_ENTRIES]; /* category for benchmark */
  } category;

  struct {
    /* linked list of benchmarks with given solution/difficulty */
    unsigned first[2][5];    /* [solution][difficulty_interval] */

    /* benchmark count with given solution/difficulty */
    unsigned n[2][5];        /* [solution][difficulty_interval] */

    unsigned next[N_POOL_ENTRIES]; /* next ptr in linked list */
  } solutiondiff;

  /* benchmark IDs */
  unsigned entries[N_POOL_ENTRIES]; /* the benchmark ID for this record */
} dpool_t;

char *prog;

dpool_t dpool;
fpool_t fpool;

/* Returns the interval the input difficulty is on:
 *   on the interval [0,1] -> returns 0
 *   on the interval (1,2] -> returns 1
 *   on the interval (2,3] -> returns 2
 *   on the interval (3,4] -> returns 3
 *   on the interval (4,5] -> returns 4 */
inline unsigned difficulty_interval(double d) {
  if(d == 0.0)
    return 0;

  assert(d > 0.0 && d <= 5.0);
  unsigned interval = ((unsigned) ceil(d)) - 1;
  assert(interval >= 0 && interval < 5);
  return interval;
}

int main(int argc, char *argv[]) {
  char last_division[256] = "", last_family[256] = "";
  char first = 1;
  unsigned lines = 1, nlines;
  unsigned seed;
  unsigned long l;
  char buf[1024];
  char *end;
  FILE *fp;

  /* get the basename of argv[0], for error messages */
  prog = strrchr(argv[0], '/');
  prog = prog ? prog + 1 : argv[0];

  if(argc != 3 && argc != 4) {
    fprintf(stderr, "usage: %s random-seed benchmarks-file\n", prog);
    exit(1);
  }

  l = strtoul(argv[1], &end, 0);
  if(*end) {
    fprintf(stderr, "%s: improper random seed `%s'\n", prog, argv[1]);
    exit(1);
  }
  if(l >= (1 << 30)) {
    fprintf(stderr, "%s: random seed must be in the range [0,2^30)\n", prog);
    exit(1);
  }

  seed = (unsigned) l;
  fprintf(stderr, "seeding with %u\n", seed);
  srandom(seed);

  if(!(fp = fopen(argv[2], "r"))) {
    fprintf(stderr, "%s: cannot open benchmarks file `%s'\n", prog, argv[2]);
    exit(1);
  }

  if(!fgets(buf, sizeof(buf), fp)) {
    fprintf(stderr, "%s: error reading file `%s' at line 1\n", prog, argv[2]);
    exit(1);
  }
  nlines = (unsigned) strtoul(buf, &end, 10);

  while(fgets(buf, sizeof(buf), fp)) {
    char *division, *family, *family_end, *s_category, *s_difficulty;
    char *s_solution, *s_benchmarkid, *file;
    double difficulty;
    unsigned benchmarkid;
    solution_t solution;
    category_t category;

    ++lines;
    size_t len = strlen(buf);
    if(buf[len - 1] != '\n') {
      fprintf(stderr, "%s: `%s' line %u too long (max len %d characters)\n",
              prog, argv[2], lines, sizeof(buf) - 2);
      exit(1);
    }

    if( !(division      = buf) ||
        !(family        = strchr(division,          ' ')) ||
        !(s_category    = strchr(family + 1,        ' ')) || 
        !(s_difficulty  = strchr(s_category + 1,    ' ')) ||
        !(s_solution    = strchr(s_difficulty + 1,  ' ')) ||
        !(s_benchmarkid = strchr(s_solution + 1,    ' ')) ||
        !(file          = strchr(s_benchmarkid + 1, ' ')) ) {
      fprintf(stderr, "%s: `%s' line %u malformed\n", prog, argv[2], lines);
      exit(1);
    }

    /* these things are pointing to the spaces _before_ their fields;
     * fix them */
    *family++ = 0;
    *s_category++ = 0;
    *s_difficulty++ = 0;
    *s_solution++ = 0;
    *s_benchmarkid++ = 0;
    *file++ = 0;

    /* truncate family name at first / */
    if(family_end = strchr(family, '/'))
      *family_end = 0;

    difficulty = strtod(s_difficulty, &end);

    if(!strcmp(s_solution, "sat"))
      solution = SAT;
    else if(!strcmp(s_solution, "unsat"))
      solution = UNSAT;
    else if(!strcmp(s_solution, "unknown"))
      solution = UNKNOWN;
    else {
      fprintf(stderr, "%s: `%s' line %u: bad solution `%s'\n",
              prog, argv[2], lines, s_solution);
      exit(1);
    }

    if((*end || difficulty < 0.0 || difficulty > 5.0) && solution != UNKNOWN) {
      fprintf(stderr, "%s: `%s' line %u: bad difficulty `%s'\n",
              prog, argv[2], lines, s_difficulty);
      exit(1);
    }

    benchmarkid = (unsigned) strtoul(s_benchmarkid, &end, 10);
    if(*end) {
      fprintf(stderr, "%s: `%s' line %u: bad benchmarkid `%s'\n",
              prog, argv[2], lines, s_benchmarkid);
      exit(1);
    }

    if(!strcmp(s_category, "check")) {
      category = CHECK;
    } else if(!strcmp(s_category, "industrial"))
      category = INDUSTRIAL;
    else if(!strcmp(s_category, "crafted"))
      category = CRAFTED;
    else if(!strcmp(s_category, "random"))
      category = RANDOM;
    else {
      fprintf(stderr, "%s: `%s' line %u: bad category `%s'\n",
              prog, argv[2], lines, s_category);
      exit(1);
    }

    /* The input line has been completely parsed at this point. */

    /* check benchmarks always included */
    if(category == CHECK) {
      puts(s_benchmarkid);
      continue;
    }

    /* unknown-status benchmarks always excluded */
    if(solution == UNKNOWN)
      continue;

    /* The structure of the rest of the input loop is as follows.  If
     * you intend to actually understand this code, it might prove
     * easiest to read the final bit first (benchmark registration),
     * then family selection, then the division selection.
     *
     * if(first input line) {
     *   do some bookkeeping
     * } else if(first input line of a new benchmark family) {
     *   do family-selection stuff: if the family we're finishing has
     *   added too many benchmarks to the division pool, remove some;
     *   then, reset family counters
     * }
     *
     * if(first input line of a new division) {
     *   do division-selection stuff: do final selection and output
     *   benchmark IDs of selected benchmarks, then reset division pool
     *   structures
     * }
     *
     * finally, register the benchmark we read from the input file by
     * adding it to the current family/division pool
     *
     */

    if(first) {
      /* first input line */
      strcpy(last_family, family);
      strcpy(last_division, division);
    } else if(strcmp(family, last_family) || strcmp(division, last_division)) {
      /* end of family; add last_family contribution to division pool */
      unsigned i, j;

      fprintf(stderr, "family %s\n  %u benchmarks", last_family, fpool.n);

      if(fpool.n > FAMILY_SIZE) {
        /* do selection to get down to FAMILY_SIZE */

        unsigned slots[2][5]; /* slots allocated for given [solution][difficulty_interval] */
        unsigned total = 0; /* total number of slots allocated */
        unsigned limited = 0;

        fprintf(stderr, "\n %4u SAT-0,%4u SAT-1,%4u SAT-2,%4u SAT-3,%4u SAT-4,%4u UNSAT-0,%4u UNSAT-1,%4u UNSAT-2,%4u UNSAT-3,%4u UNSAT-4 [eligible non-check]",
                fpool.solutiondiff.n[SAT][0],
                fpool.solutiondiff.n[SAT][1],
                fpool.solutiondiff.n[SAT][2],
                fpool.solutiondiff.n[SAT][3],
                fpool.solutiondiff.n[SAT][4],
                fpool.solutiondiff.n[UNSAT][0],
                fpool.solutiondiff.n[UNSAT][1],
                fpool.solutiondiff.n[UNSAT][2],
                fpool.solutiondiff.n[UNSAT][3],
                fpool.solutiondiff.n[UNSAT][4]);

        /* First, allocate slots to [solution][difficulty] pairs. */
        /* In "limited", we track the number of [solution][difficulty]
         * pairs for which the allocation is maximal (there are no
         * more benchmarks available in the familya beyond the current
         * allocation). */

        /* i is solution, j is difficulty interval */
        for(i = 0; i < 2; ++i)
          for(j = 0; j < 5; ++j)
            if(fpool.solutiondiff.n[i][j] <= FAMILY_SIZE / 10) {
              /* not enough benchmarks in family to include 10% of the
               * family's budget with this solution/difficulty, reduce
               * the allocation and mark as limited */
              total += slots[i][j] = fpool.solutiondiff.n[i][j];
              ++limited;
            } else {
              /* there are enough in the family, so allocate 10% */
              total += slots[i][j] = FAMILY_SIZE / 10;
            }

        /* Our total allocation can be less than FAMILY_SIZE, of
         * course, since some [solution][difficulty] pairs may not
         * have had enough benchmarks.  In each iteration of this
         * loop, we allocate "each" (which equals
         * (FAMILY_SIZE - total) / (10 - limited)) more slots to
         * each [solution][difficulty] pair that has enough
         * benchmarks, to eat up this slack.  We keep track of
         * "limited", like above. */

        /* (limited < 10): Note if all [solution][difficulty] pairs
         * are limited by the number of available benchmarks, we're
         * done: the allocation includes ALL benchmarks! */
        while(total < FAMILY_SIZE && limited < 10) {

          unsigned each = (FAMILY_SIZE - total) / (10 - limited);

          /* if each == 0, no more slot-allocation to do here, but may
           * be some below in the following loop (see below) */
          if(each == 0)
            break;

          /* for each solution/difficulty... */
          for(i = 0; i < 2; ++i)
            for(j = 0; j < 5; ++j)
              if(slots[i][j] < fpool.solutiondiff.n[i][j]) {
                /* ...allocate up to "each" slots */
                if(slots[i][j] + each > fpool.solutiondiff.n[i][j]) {
                  total -= slots[i][j];
                  total += slots[i][j] = fpool.solutiondiff.n[i][j];
                  ++limited;
                } else {
                  slots[i][j] += each;
                  total += each;
                  if(slots[i][j] == fpool.solutiondiff.n[i][j])
                    ++limited;
                }
              }
        }

        assert(limited == 10 || FAMILY_SIZE - total < 10);

        /* If we exited the above loop because total == FAMILY_SIZE or
         * because limited == 10, we're done.  But if we exited
         * because "each" was 0, there may be up to 9 additional slots
         * to allocate (due to the integer division).  Here, we
         * allocate those randomly across the [solution][difficulty]
         * pairs, making sure never to ever give a pair more than
         * *one* extra slot. */
        if(total < FAMILY_SIZE && limited < 10) {
          char extra_slot[2][5];
          unsigned extra_allocations = 0;

          memset(extra_slot, 0, sizeof(extra_slot));

          do {
            fprintf(stderr, "\n %4u%cSAT-0,%4u%cSAT-1,%4u%cSAT-2,%4u%cSAT-3,%4u%cSAT-4,%4u%cUNSAT-0,%4u%cUNSAT-1,%4u%cUNSAT-2,%4u%cUNSAT-3,%4u%cUNSAT-4 [fpool allotment*,%u rounds remain,%u eligible]",
                    slots[SAT][0], slots[SAT][0] == fpool.solutiondiff.n[SAT][0] ? '*' : ' ',
                    slots[SAT][1], slots[SAT][1] == fpool.solutiondiff.n[SAT][1] ? '*' : ' ',
                    slots[SAT][2], slots[SAT][2] == fpool.solutiondiff.n[SAT][2] ? '*' : ' ',
                    slots[SAT][3], slots[SAT][3] == fpool.solutiondiff.n[SAT][3] ? '*' : ' ',
                    slots[SAT][4], slots[SAT][4] == fpool.solutiondiff.n[SAT][4] ? '*' : ' ',
                    slots[UNSAT][0], slots[UNSAT][0] == fpool.solutiondiff.n[UNSAT][0] ? '*' : ' ',
                    slots[UNSAT][1], slots[UNSAT][1] == fpool.solutiondiff.n[UNSAT][1] ? '*' : ' ',
                    slots[UNSAT][2], slots[UNSAT][2] == fpool.solutiondiff.n[UNSAT][2] ? '*' : ' ',
                    slots[UNSAT][3], slots[UNSAT][3] == fpool.solutiondiff.n[UNSAT][3] ? '*' : ' ',
                    slots[UNSAT][4], slots[UNSAT][4] == fpool.solutiondiff.n[UNSAT][4] ? '*' : ' ',
                    FAMILY_SIZE - total,
                    10 - limited - extra_allocations);

            unsigned n = random() % (10 - limited - extra_allocations);
            /* now find the nth pair that can have a larger allocation
             * (that wasn't already given an extra allocation) and
             * increase its allocation by one. */
            for(i = 0; i < 2; ++i)
              for(j = 0; j < 5; ++j)
                if(extra_slot[i][j] == 0 &&
                   slots[i][j] < fpool.solutiondiff.n[i][j] &&
                   n-- == 0) {
                  ++total;
                  extra_slot[i][j] = 1;
                  if(++slots[i][j] == fpool.solutiondiff.n[i][j])
                    ++limited;
                  else ++extra_allocations;
                  /* break out of here */
                  goto family_next_iteration;
                }
          family_next_iteration:
            ;
          } while(total < FAMILY_SIZE && limited < 10);
        }

        assert(total <= FAMILY_SIZE);
        assert(limited <= 10);

        fprintf(stderr, "\n %4u%cSAT-0,%4u%cSAT-1,%4u%cSAT-2,%4u%cSAT-3,%4u%cSAT-4,%4u%cUNSAT-0,%4u%cUNSAT-1,%4u%cUNSAT-2,%4u%cUNSAT-3,%4u%cUNSAT-4 [fpool allotment]\n",
                slots[SAT][0], slots[SAT][0] == fpool.solutiondiff.n[SAT][0] ? '*' : ' ',
                slots[SAT][1], slots[SAT][1] == fpool.solutiondiff.n[SAT][1] ? '*' : ' ',
                slots[SAT][2], slots[SAT][2] == fpool.solutiondiff.n[SAT][2] ? '*' : ' ',
                slots[SAT][3], slots[SAT][3] == fpool.solutiondiff.n[SAT][3] ? '*' : ' ',
                slots[SAT][4], slots[SAT][4] == fpool.solutiondiff.n[SAT][4] ? '*' : ' ',
                slots[UNSAT][0], slots[UNSAT][0] == fpool.solutiondiff.n[UNSAT][0] ? '*' : ' ',
                slots[UNSAT][1], slots[UNSAT][1] == fpool.solutiondiff.n[UNSAT][1] ? '*' : ' ',
                slots[UNSAT][2], slots[UNSAT][2] == fpool.solutiondiff.n[UNSAT][2] ? '*' : ' ',
                slots[UNSAT][3], slots[UNSAT][3] == fpool.solutiondiff.n[UNSAT][3] ? '*' : ' ',
                slots[UNSAT][4], slots[UNSAT][4] == fpool.solutiondiff.n[UNSAT][4] ? '*' : ' ');

        for(i = 0; i < 2; ++i)
          for(j = 0; j < 5; ++j) {
            /*fprintf(stderr,"beforeward:[%u][%u] %u slots, fpool has %u, dpool has %u\n", i, j, slots[i][j], fpool.solutiondiff.n[i][j], dpool.solutiondiff.n[i][j]);
            fprintf(stderr,"\nhave [n=%u]:\n", dpool.solutiondiff.n[i][j]);
            if(dpool.solutiondiff.n[i][j]) {
              unsigned x = dpool.solutiondiff.first[i][j];
              int k = 0;
              do {
                fprintf(stderr, "%3u[%u][%u] :: %3u %5u\n", k, i, j, x, dpool.entries[x]);
                x = dpool.solutiondiff.next[x];
              } while(++k < dpool.solutiondiff.n[i][j]);
            }*/

            /* cut entries randomly from the division pool until we
             * reach our budget */
            while(slots[i][j] < fpool.solutiondiff.n[i][j]) {
              long n = random() % fpool.solutiondiff.n[i][j];
              unsigned *x = &dpool.solutiondiff.first[i][j];
              while(n--)
                x = &dpool.solutiondiff.next[*x];

              //fprintf(stderr,"cutting %3u %5u [%u][%u], next=%3u %5u\n",*x,dpool.entries[*x],i,j,dpool.solutiondiff.next[*x],dpool.entries[dpool.solutiondiff.next[*x]]);

              /*dpool.category.values[*x] = -1;*/

              *x = dpool.solutiondiff.next[*x];
              --fpool.solutiondiff.n[i][j];
              --dpool.solutiondiff.n[i][j];
              --fpool.n;
              --dpool.n;
            }
            /*fprintf(stderr,"afterward: [%u][%u] %u slots, fpool has %u, dpool has %u\n", i, j, slots[i][j], fpool.solutiondiff.n[i][j], dpool.solutiondiff.n[i][j]);
            fprintf(stderr,"\nhave [n=%u]:\n", dpool.solutiondiff.n[i][j]);
            if(dpool.solutiondiff.n[i][j]) {
              unsigned x = dpool.solutiondiff.first[i][j];
              int k = 0;
              do {
                fprintf(stderr, "%3u[%u][%u] :: %3u %5u\n", k, i, j, x, dpool.entries[x]);
                x = dpool.solutiondiff.next[x];
              } while(++k < dpool.solutiondiff.n[i][j]);
            }*/
          }
      } else {
        fprintf(stderr, ", all go to division pool\n %4u SAT-0,%4u SAT-1,%4u SAT-2,%4u SAT-3,%4u SAT-4,%4u UNSAT-0,%4u UNSAT-1,%4u UNSAT-2,%4u UNSAT-3,%4u UNSAT-4 [to division pool]\n",
                fpool.solutiondiff.n[SAT][0],
                fpool.solutiondiff.n[SAT][1],
                fpool.solutiondiff.n[SAT][2],
                fpool.solutiondiff.n[SAT][3],
                fpool.solutiondiff.n[SAT][4],
                fpool.solutiondiff.n[UNSAT][0],
                fpool.solutiondiff.n[UNSAT][1],
                fpool.solutiondiff.n[UNSAT][2],
                fpool.solutiondiff.n[UNSAT][3],
                fpool.solutiondiff.n[UNSAT][4]);
      }
      /*fprintf(stderr, "\nafter, in dpool:\n  %u easySAT,\n  %u hardSAT,\n  %u easyUNSAT\n  %u hardUNSAT\n\n", dpool.solutiondiff.n[SAT][EASY], dpool.solutiondiff.n[SAT][HARD], dpool.solutiondiff.n[UNSAT][EASY], dpool.solutiondiff.n[UNSAT][HARD]);
      for(i = 0; i < 2; ++i)
        for(j = 0; j < 2; ++j) {
          fprintf(stderr,"\nhave [n=%u]:\n", dpool.solutiondiff.n[i][j]);
          if(dpool.solutiondiff.n[i][j]) {
            unsigned x = dpool.solutiondiff.first[i][j];
            int k = 0;
            do {
              fprintf(stderr, "%3u[%u][%u] :: %3u %5u\n", k, i, j, x, dpool.entries[x]);
              x = dpool.solutiondiff.next[x];
            } while(++k < dpool.solutiondiff.n[i][j]);
          }
        }*/

      /* reset family counters */
      fpool.n = 0;
      memset(fpool.solutiondiff.n, 0, sizeof(fpool.solutiondiff.n));

      strcpy(last_family, family);
    }
    if(!first && strcmp(division, last_division)) {
      /* end of division; select from division pool */
      unsigned i, j, x, c;

      /* SPECIAL HACK SMT-COMP 2009 -- see notes at top of source file */
      /*unsigned reduction_factor = 1;
      if(!strcmp(last_division, "QF_IDL"))
        reduction_factor = 2;*/
      /* END HACK */

      fprintf(stderr, "division %s, %u benchmarks in pool", last_division, dpool.n);
      fprintf(stderr, "\n %4u SAT-0,%4u SAT-1,%4u SAT-2,%4u SAT-3,%4u SAT-4,%4u UNSAT-0,%4u UNSAT-1,%4u UNSAT-2,%4u UNSAT-3,%4u UNSAT-4 [pool totals]",
              dpool.solutiondiff.n[SAT][0],
              dpool.solutiondiff.n[SAT][1],
              dpool.solutiondiff.n[SAT][2],
              dpool.solutiondiff.n[SAT][3],
              dpool.solutiondiff.n[SAT][4],
              dpool.solutiondiff.n[UNSAT][0],
              dpool.solutiondiff.n[UNSAT][1],
              dpool.solutiondiff.n[UNSAT][2],
              dpool.solutiondiff.n[UNSAT][3],
              dpool.solutiondiff.n[UNSAT][4]);

      /* first, generate category reverse map */

      dpool.category.nc[INDUSTRIAL] = 0;
      dpool.category.nc[CRAFTED] = 0;
      dpool.category.nc[RANDOM] = 0;
      for(i = 0; i < 2; ++i)
        for(j = 0; j < 5; ++j) {
          /*fprintf(stderr,"\nhave [n=%u]:\n", dpool.solutiondiff.n[i][j]);
          if(dpool.solutiondiff.n[i][j]) {
            unsigned x = dpool.solutiondiff.first[i][j];
            int k = 0;
            do {
              fprintf(stderr, "%3u[%u][%u] :: %3u %5u\n", k, i, j, x, dpool.entries[x]);
              x = dpool.solutiondiff.next[x];
            } while(++k < dpool.solutiondiff.n[i][j]);
          }*/

          dpool.category.n[INDUSTRIAL][i][j] = 0;
          dpool.category.n[CRAFTED][i][j] = 0;
          dpool.category.n[RANDOM][i][j] = 0;
          if(dpool.solutiondiff.n[i][j]) {
            int k = 1;
            x = dpool.solutiondiff.first[i][j];
            do {
              category_t cat = dpool.category.values[x];
              assert(cat >= 0 && cat <= 2);
              ++dpool.category.n[cat][i][j];
              ++dpool.category.nc[cat];
              /* maintain category linked list */
              dpool.category.next[x] = dpool.category.first[cat][i][j];
              dpool.category.first[cat][i][j] = x;
              x = dpool.solutiondiff.next[x];
            } while(++k <= dpool.solutiondiff.n[i][j]);
          }
        }

      fprintf(stderr, "\n %4u industr,%4u crafted,%4u random                                                                                   [pool totals]",
              dpool.category.nc[INDUSTRIAL],
              dpool.category.nc[CRAFTED],
              dpool.category.nc[RANDOM]);
      fprintf(stderr, "\n %4u SAT-0,%4u SAT-1,%4u SAT-2,%4u SAT-3,%4u SAT-4,%4u UNSAT-0,%4u UNSAT-1,%4u UNSAT-2,%4u UNSAT-3,%4u UNSAT-4 [industrial]",
              dpool.category.n[INDUSTRIAL][SAT][0],
              dpool.category.n[INDUSTRIAL][SAT][1],
              dpool.category.n[INDUSTRIAL][SAT][2],
              dpool.category.n[INDUSTRIAL][SAT][3],
              dpool.category.n[INDUSTRIAL][SAT][4],
              dpool.category.n[INDUSTRIAL][UNSAT][0],
              dpool.category.n[INDUSTRIAL][UNSAT][1],
              dpool.category.n[INDUSTRIAL][UNSAT][2],
              dpool.category.n[INDUSTRIAL][UNSAT][3],
              dpool.category.n[INDUSTRIAL][UNSAT][4]);
      fprintf(stderr, "\n %4u SAT-0,%4u SAT-1,%4u SAT-2,%4u SAT-3,%4u SAT-4,%4u UNSAT-0,%4u UNSAT-1,%4u UNSAT-2,%4u UNSAT-3,%4u UNSAT-4 [crafted]",
              dpool.category.n[CRAFTED][SAT][0],
              dpool.category.n[CRAFTED][SAT][1],
              dpool.category.n[CRAFTED][SAT][2],
              dpool.category.n[CRAFTED][SAT][3],
              dpool.category.n[CRAFTED][SAT][4],
              dpool.category.n[CRAFTED][UNSAT][0],
              dpool.category.n[CRAFTED][UNSAT][1],
              dpool.category.n[CRAFTED][UNSAT][2],
              dpool.category.n[CRAFTED][UNSAT][3],
              dpool.category.n[CRAFTED][UNSAT][4]);
      fprintf(stderr, "\n %4u SAT-0,%4u SAT-1,%4u SAT-2,%4u SAT-3,%4u SAT-4,%4u UNSAT-0,%4u UNSAT-1,%4u UNSAT-2,%4u UNSAT-3,%4u UNSAT-4 [random]",
              dpool.category.n[RANDOM][SAT][0],
              dpool.category.n[RANDOM][SAT][1],
              dpool.category.n[RANDOM][SAT][2],
              dpool.category.n[RANDOM][SAT][3],
              dpool.category.n[RANDOM][SAT][4],
              dpool.category.n[RANDOM][UNSAT][0],
              dpool.category.n[RANDOM][UNSAT][1],
              dpool.category.n[RANDOM][UNSAT][2],
              dpool.category.n[RANDOM][UNSAT][3],
              dpool.category.n[RANDOM][UNSAT][4]);

      unsigned cslots[3] = CATEGORY_ALLOTMENT;
      /* SPECIAL HACK SMT-COMP 2009 -- see notes at top of source file */
      //cslots[0] /= reduction_factor;
      //cslots[1] /= reduction_factor;
      //cslots[2] /= reduction_factor;
      /* END HACK */
      if(dpool.category.nc[RANDOM] < cslots[RANDOM]) {
        cslots[INDUSTRIAL] += cslots[RANDOM] - dpool.category.nc[RANDOM];
        cslots[RANDOM] = dpool.category.nc[RANDOM];
      }
      if(dpool.category.nc[CRAFTED] < cslots[CRAFTED]) {
        cslots[INDUSTRIAL] += cslots[CRAFTED] - dpool.category.nc[CRAFTED];
        cslots[CRAFTED] = dpool.category.nc[CRAFTED];
        if(dpool.category.nc[INDUSTRIAL] < cslots[INDUSTRIAL]) {
          cslots[RANDOM] += cslots[INDUSTRIAL] - dpool.category.nc[INDUSTRIAL];
          cslots[INDUSTRIAL] = dpool.category.nc[INDUSTRIAL];
        }
      } else if(dpool.category.nc[INDUSTRIAL] < cslots[INDUSTRIAL]) {
        cslots[CRAFTED] += cslots[INDUSTRIAL] - dpool.category.nc[INDUSTRIAL];
        cslots[INDUSTRIAL] = dpool.category.nc[INDUSTRIAL];
      }

      fprintf(stderr, "\n %4u industr,%4u crafted,%4u random                                                                                   [slot allotments]\n",
              cslots[INDUSTRIAL],
              cslots[CRAFTED],
              cslots[RANDOM]);

      //assert(cslots[INDUSTRIAL] + cslots[CRAFTED] + cslots[RANDOM] == N / reduction_factor);/* SMT-COMP 2009 HACK */
      assert(cslots[INDUSTRIAL] + cslots[CRAFTED] + cslots[RANDOM] == N);

      if(dpool.category.nc[INDUSTRIAL] < cslots[INDUSTRIAL] ||
         dpool.category.nc[CRAFTED] < cslots[CRAFTED] ||
         dpool.category.nc[RANDOM] < cslots[RANDOM]) {
        fprintf(stderr, "WARNING: division %s does not have enough benchmarks\n", last_division);
        fprintf(stderr, "    avail industrial in dpool:%4u  - I want:%4u\n", dpool.category.nc[INDUSTRIAL], cslots[INDUSTRIAL]);
        fprintf(stderr, "    avail crafted in dpool:   %4u  - I want:%4u\n", dpool.category.nc[CRAFTED], cslots[CRAFTED]);
        fprintf(stderr, "    avail random in dpool:    %4u  - I want:%4u\n", dpool.category.nc[RANDOM], cslots[RANDOM]);

        if(dpool.category.nc[INDUSTRIAL] < cslots[INDUSTRIAL])
          cslots[INDUSTRIAL] = dpool.category.nc[INDUSTRIAL];
        if(dpool.category.nc[CRAFTED] < cslots[CRAFTED])
          cslots[CRAFTED] = dpool.category.nc[CRAFTED];
        if(dpool.category.nc[RANDOM] < cslots[RANDOM])
          cslots[RANDOM] = dpool.category.nc[RANDOM];
      }

      for(c = 0; c < 3; ++c) {/* for(each category c) */
        unsigned slots[2][5]; /* [solution][difficulty] */
        unsigned total = 0;
        unsigned limited = 0;

        fprintf(stderr, " %4u SAT-0,%4u SAT-1,%4u SAT-2,%4u SAT-3,%4u SAT-4,%4u UNSAT-0,%4u UNSAT-1,%4u UNSAT-2,%4u UNSAT-3,%4u UNSAT-4 [cat %d avail]\n",
                dpool.category.n[c][SAT][0],
                dpool.category.n[c][SAT][1],
                dpool.category.n[c][SAT][2],
                dpool.category.n[c][SAT][3],
                dpool.category.n[c][SAT][4],
                dpool.category.n[c][UNSAT][0],
                dpool.category.n[c][UNSAT][1],
                dpool.category.n[c][UNSAT][2],
                dpool.category.n[c][UNSAT][3],
                dpool.category.n[c][UNSAT][4],
                c);

        /* i is solution, j is difficulty interval */
        for(i = 0; i < 2; ++i)
          for(j = 0; j < 5; ++j)
            if(dpool.category.n[c][i][j] <= cslots[c] / 10) {
              /* not enough benchmarks to include 10% with this
               * solution/difficulty, reduce the allocation and mark
               * as limited */
              total += slots[i][j] = dpool.category.n[c][i][j];
              ++limited;
            } else {
              /* there are enough, so allocate 10% */
              total += slots[i][j] = cslots[c] / 10;
            }

        /* Our total allocation can be less than the slots allocated,
         * of course, since some [solution][difficulty] pairs may not
         * have had enough benchmarks.  In each iteration of this
         * loop, we allocate "each" (which equals
         * (slot_allocation - total) / (10 - limited)) more slots to
         * each [solution][difficulty] pair that has enough
         * benchmarks, to eat up this slack.  We keep track of
         * "limited", like above. */

        /* (limited < 10): Note if all [solution][difficulty] pairs
         * are limited by the number of available benchmarks, we're
         * done: the allocation includes ALL benchmarks! */
        while(total < cslots[c] && limited < 10) {

          unsigned each = (cslots[c] - total) / (10 - limited);

          /* if each == 0, no more slot-allocation to do here, but may
           * be some below in the following loop (see below) */
          if(each == 0)
            break;

          /* for each solution/difficulty... */
          for(i = 0; i < 2; ++i)
            for(j = 0; j < 5; ++j)
              if(slots[i][j] < dpool.category.n[c][i][j]) {
                /* ...allocate up to "each" slots */
                if(slots[i][j] + each > dpool.category.n[c][i][j]) {
                  total -= slots[i][j];
                  total += slots[i][j] = dpool.category.n[c][i][j];
                  ++limited;
                } else {
                  slots[i][j] += each;
                  total += each;
                  if(slots[i][j] == dpool.category.n[c][i][j])
                    ++limited;
                }
              }
        }

        assert(cslots[c] - total < 10);

        /* If we exited the above loop because total == FAMILY_SIZE or
         * because limited == 10, we're done.  But if we exited
         * because "each" was 0, there may be up to 9 additional slots
         * to allocate (due to the integer division).  Here, we
         * allocate those randomly across the [solution][difficulty]
         * pairs, making sure never to ever give a pair more than
         * *one* extra slot. */
        if(total < cslots[c] && limited < 10) {
          char extra_slot[2][5];
          unsigned extra_allocations = 0;

          memset(extra_slot, 0, sizeof(extra_slot));

          do {
            fprintf(stderr, " %4u%cSAT-0,%4u%cSAT-1,%4u%cSAT-2,%4u%cSAT-3,%4u%cSAT-4,%4u%cUNSAT-0,%4u%cUNSAT-1,%4u%cUNSAT-2,%4u%cUNSAT-3,%4u%cUNSAT-4 [cat %d allotment*,%u rounds remain,%u eligible]\n",
                    slots[SAT][0], slots[SAT][0] == dpool.category.n[c][SAT][0] ? '*' : ' ',
                    slots[SAT][1], slots[SAT][1] == dpool.category.n[c][SAT][1] ? '*' : ' ',
                    slots[SAT][2], slots[SAT][2] == dpool.category.n[c][SAT][2] ? '*' : ' ',
                    slots[SAT][3], slots[SAT][3] == dpool.category.n[c][SAT][3] ? '*' : ' ',
                    slots[SAT][4], slots[SAT][4] == dpool.category.n[c][SAT][4] ? '*' : ' ',
                    slots[UNSAT][0], slots[UNSAT][0] == dpool.category.n[c][UNSAT][0] ? '*' : ' ',
                    slots[UNSAT][1], slots[UNSAT][1] == dpool.category.n[c][UNSAT][1] ? '*' : ' ',
                    slots[UNSAT][2], slots[UNSAT][2] == dpool.category.n[c][UNSAT][2] ? '*' : ' ',
                    slots[UNSAT][3], slots[UNSAT][3] == dpool.category.n[c][UNSAT][3] ? '*' : ' ',
                    slots[UNSAT][4], slots[UNSAT][4] == dpool.category.n[c][UNSAT][4] ? '*' : ' ',
                    c,
                    cslots[c] - total,
                    10 - limited - extra_allocations);

            unsigned n = random() % (10 - limited - extra_allocations);
            /* now find the nth pair that can have a larger allocation
             * (that wasn't already given an extra allocation) and
             * increase its allocation by one. */
            for(i = 0; i < 2; ++i)
              for(j = 0; j < 5; ++j)
                if(extra_slot[i][j] == 0 &&
                   slots[i][j] < dpool.category.n[c][i][j] &&
                   n-- == 0) {
                  ++total;
                  extra_slot[i][j] = 1;
                  if(++slots[i][j] == dpool.category.n[c][i][j])
                    ++limited;
                  else ++extra_allocations;
                  /* break out of here */
                  goto division_next_iteration;
                }
          division_next_iteration:
            ;
          } while(total < cslots[c] && limited < 10);
        }

        assert(total <= cslots[c]);
        assert(limited <= 10);

        fprintf(stderr, " %4u%cSAT-0,%4u%cSAT-1,%4u%cSAT-2,%4u%cSAT-3,%4u%cSAT-4,%4u%cUNSAT-0,%4u%cUNSAT-1,%4u%cUNSAT-2,%4u%cUNSAT-3,%4u%cUNSAT-4 [cat %d allotment]\n",
                slots[SAT][0], slots[SAT][0] == dpool.category.n[c][SAT][0] ? '*' : ' ',
                slots[SAT][1], slots[SAT][1] == dpool.category.n[c][SAT][1] ? '*' : ' ',
                slots[SAT][2], slots[SAT][2] == dpool.category.n[c][SAT][2] ? '*' : ' ',
                slots[SAT][3], slots[SAT][3] == dpool.category.n[c][SAT][3] ? '*' : ' ',
                slots[SAT][4], slots[SAT][4] == dpool.category.n[c][SAT][4] ? '*' : ' ',
                slots[UNSAT][0], slots[UNSAT][0] == dpool.category.n[c][UNSAT][0] ? '*' : ' ',
                slots[UNSAT][1], slots[UNSAT][1] == dpool.category.n[c][UNSAT][1] ? '*' : ' ',
                slots[UNSAT][2], slots[UNSAT][2] == dpool.category.n[c][UNSAT][2] ? '*' : ' ',
                slots[UNSAT][3], slots[UNSAT][3] == dpool.category.n[c][UNSAT][3] ? '*' : ' ',
                slots[UNSAT][4], slots[UNSAT][4] == dpool.category.n[c][UNSAT][4] ? '*' : ' ',
                c);

        for(i = 0; i < 2; ++i)
          for(j = 0; j < 5; ++j) {
            /*if(dpool.category.n[c][i][j]) {
              unsigned x = dpool.category.first[c][i][j];
              int k = 0;
              do {
                fprintf(stderr, "%3u[%u][%u][%u] :: %5u\n", k, c, i, j, dpool.entries[x]);
                x = dpool.category.next[x];
              } while(++k < dpool.category.n[c][i][j]);
            }*/

            /* select entries randomly from the category until we
             * reach our budget; remove them from the category so we
             * don't select one twice. */
            while(slots[i][j]--) {
              long n = random() % dpool.category.n[c][i][j];
              unsigned *x = &dpool.category.first[c][i][j];
              //printf("%5u ", n);
              //fprintf(stderr,"%5u ", n);
              while(n--)
                x = &dpool.category.next[*x];

              //printf("%u %u %u %u\n", c, i, j, dpool.entries[*x]);
              //fprintf(stderr,"%u %u %u %u\n", c, i, j, dpool.entries[*x]);
              printf("%u\n", dpool.entries[*x]);

              *x = dpool.category.next[*x];
              --dpool.category.n[c][i][j];
            }
          }
      }/* end: for(each category c) */
      fflush(stderr);
      fflush(stdout);

      /* reset division counters */
      dpool.n = 0;
      dpool.alloc = 0;
      memset(dpool.solutiondiff.n, 0, sizeof(dpool.solutiondiff.n));

      strcpy(last_division, division);
    }
    first = 0;

    /* register the benchmark from the input line we just read */

    assert(dpool.alloc < N_POOL_ENTRIES);
    /* register the category */
    dpool.category.values[dpool.alloc] = category;
    /* family/division pool counters */
    ++fpool.solutiondiff.n[solution][difficulty_interval(difficulty)];
    ++dpool.solutiondiff.n[solution][difficulty_interval(difficulty)];
    /* put it on [solution][difficulty] linked list */
    dpool.solutiondiff.next[dpool.alloc] =
      dpool.solutiondiff.first[solution][difficulty_interval(difficulty)];
    dpool.solutiondiff.first[solution][difficulty_interval(difficulty)] = dpool.alloc;
    /* remember the benchmarkid */
    dpool.entries[dpool.alloc++] = benchmarkid;
    /* update pool totals */
    ++dpool.n;
    ++fpool.n;

    //fprintf(stderr,"added %3u %5u [%u][%u], next=%3u %5u\n",dpool.alloc-1,benchmarkid,solution,difficulty_interval(difficulty),dpool.solutiondiff.next[dpool.alloc-1],dpool.entries[dpool.solutiondiff.next[dpool.alloc-1]]);

    /*
    fprintf(stderr,"added : %5u\n", benchmarkid);
    if(dpool.solutiondiff.n[solution][difficulty_interval(difficulty)]) {
      unsigned x = dpool.solutiondiff.first[solution][difficulty_interval(difficulty)];
      int k = 0;
      do {
        fprintf(stderr, "%3u[%u][%u] :: %5u\n", k, solution, difficulty_interval(difficulty), dpool.entries[x]);
        x = dpool.solutiondiff.next[x];
      } while(++k < dpool.solutiondiff.n[solution][difficulty_interval(difficulty)]);
    }
    */
  }

  if(!feof(fp)) {
    fprintf(stderr, "%s: error reading file `%s' at line %u/%u\n",
            prog, argv[1], lines, nlines);
    exit(1);
  }

  fclose(fp);

  return 0;
}
