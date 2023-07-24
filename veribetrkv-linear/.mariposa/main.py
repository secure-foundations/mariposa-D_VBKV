import os

# transitively list imported dafny files from Bundle
def get_includes():
    os.system(".dafny/dafny/Scripts/dafny /printIncludes:Transitive Impl/Bundle.i.dfy /noVerify > .mariposa/imports.txt")

# keep only the unique dafny files
def get_unique_inlcudes():
    os.system("cat .mariposa/imports.txt | cut -d ';' -f 1 | xargs -n 1 realpath | sort | uniq > .mariposa/unique_imports.txt")

nl_enable_files = ["lib/Math/Nonlinear.i.dfy",
    "lib/Base/mathematics.i.dfy",
    "Impl/BookkeepingModel.i.dfy",
    "Impl/IOImpl.i.dfy",
    "Impl/IOModel.i.dfy",
    "Impl/SyncImpl.i.dfy",
    "Impl/BookkeepingImpl.i.dfy",
    "lib/Base/SetBijectivity.i.dfy",
    "lib/Marshalling/GenericMarshalling.i.dfy",
    "lib/Buckets/BucketFlushModel.i.dfy",
    "lib/Buckets/PackedStringArray.i.dfy",
    "lib/Base/Sequences.i.dfy",
    "BlockCacheSystem/DiskLayout.i.dfy",
    "ByteBlockCacheSystem/Marshalling.i.dfy",
    "ByteBlockCacheSystem/JournalBytes.i.dfy",
    "PivotBetree/Bounds.i.dfy",
    "Impl/Mkfs.i.dfy",
    "Impl/MkfsModel.i.dfy",
    "Impl/MarshallingImpl.i.dfy"]

nl_enable_files = set([os.path.realpath(f) for f in nl_enable_files])

for file_path in open(".mariposa/unique_imports.txt").readlines():
    file_path = file_path.strip() 
    # do not give a long time for verification, we only need the query
    command = ".dafny/dafny/Scripts/dafny /timeLimit:1 /compile:0 /proverLog:.mariposa/queries/@FILE@xxx@PROC@ " + file_path
    if file_path not in nl_enable_files:
        command += " /noNLarith"
    print(command) 
    
