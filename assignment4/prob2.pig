register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
-- later you will load to other files, example:
--raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 
-- Compute for the whole damn data set
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-\*' USING TextLoader as (line:chararray); 


-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

--group the n-triples by subject column
subjects = group ntriples by (subject) PARALLEL 50;

-- flatten the subjects out (because group by produces a tuple of each subject
-- in the first column, and we want each subject ot be a string, not a tuple),
-- and count the number of tuples associated with each subject
count_by_subject = foreach subjects 
    generate flatten($0) as subject, COUNT($1) as count 
    PARALLEL 50;

subject_counts_by_count = group count_by_subject by (count) PARALLEL 50;

histogram = foreach subject_counts_by_count
    generate flatten($0) as x, COUNT($1) as y
    PARALLEL 50;

--order the resulting tuples by their count in descending order
-- count_by_subject_ordered = order count_by_subject by (count)  PARALLEL 50;

-- store the results in the folder /user/hadoop/example-results
store histogram into '/user/hadoop/prob2' using PigStorage();
-- Alternatively, you can store the results in S3, see instructions:
-- store count_by_subject_ordered into 's3n://superman/example-results';
