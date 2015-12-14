register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
--raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
-- later you will load to other files, example:
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

filtered = filter ntriples by subject matches '.*rdfabout.com.*';
filtered_copy = foreach filtered generate subject as subject2, predicate as predicate2, object as object2;

joined = join filtered by object, filtered_copy by subject2;
deduped = distinct joined;

store deduped into '/user/hadoop/prob3' using PigStorage();
