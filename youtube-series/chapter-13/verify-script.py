"""Replay the recording guide in a temporary directory, never the live checkout."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
REPO = Path('/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down-ep13')
RECORDING = REPO.with_name('deep-learning-all-the-way-down')
TEMP = Path(tempfile.mkdtemp(prefix='dlatwd-ch13-'))
RESULTS = []
def run(args, cwd=TEMP):
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=240)
    if result.returncode:
        raise RuntimeError(' '.join(map(str,args))+'\n'+result.stdout)
    return result.stdout
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
original_hash = digest(RECORDING/'main.cpp')
files = {}
for name in ['main.cpp','mnist_reader.hpp','scalar_autograd.cpp']:
    files[name] = run(['git','show','c9918e8:'+name],REPO)
    (TEMP/name).write_text(files[name])
script = (HERE/'script.md').read_text()
events = json.loads((HERE/'migration-edits.json').read_text())
literal = re.findall(r'<!-- edit: (\S+) file: (\S+) -->\s*\*\*Before\*\*\s*```cpp\n(.*?)\n```\s*\*\*After\*\*\s*```cpp\n(.*?)\n```',script,re.S)
assert [(e['id'],e['path'],e['before'],e['after']) for e in events if 'id' in e] == literal
assert [e['checkpoint'] for e in events if 'checkpoint' in e] == re.findall(r'<!-- checkpoint: (\S+) -->',script)
compiler = os.environ.get('CXX','clang++')
def compile_main(name,execute=False):
    source=TEMP/(name+'.cpp');source.write_text(files['main.cpp'])
    binary=TEMP/name
    run([compiler,'-std=c++23','-O2',str(source),'-o',str(binary)])
    output=run([str(binary)],RECORDING) if execute else ''
    RESULTS.append({'checkpoint':name,'compiled':True,'executed':execute,'output':output})
    print(name+': PASS',flush=True)
    return output
baseline_output=compile_main('baseline',True)
for e in events:
    if 'id' in e:
        path=e['path'];old=files.get(path,'');before=e['before']
        assert (old.count(before)==1) if before else not old,e['id']
        files[path]=old.replace(before,e['after'],1) if before else e['after']
        target=TEMP/path;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(files[path])
    elif 'move' in e:
        files[e['to']]=files.pop(e['move'])
        (TEMP/e['move']).rename(TEMP/e['to'])
    elif 'delete' in e:
        assert not files.pop(e['delete']).strip()
        (TEMP/e['delete']).unlink()
    elif e['checkpoint'] in ['parent-mapping-complete','node-constructor-complete']:
        compile_main(e['checkpoint'])
    elif e['checkpoint']=='logical-migration-complete':
        assert compile_main(e['checkpoint'],True)==baseline_output
    elif e['checkpoint']=='split-library-complete':
        run(['cmake','-S','.', '-B','build/debug','-G','Ninja',
             '-DCMAKE_BUILD_TYPE=Debug',
             '-DFETCHCONTENT_SOURCE_DIR_GOOGLETEST='+str(REPO/'build/debug/_deps/googletest-src')])
        run(['cmake','--build','build/debug','-j','4'])
        output=run(['ctest','--test-dir','build/debug','--output-on-failure'])
        assert '0 tests failed out of 41' in output
        RESULTS.append({'checkpoint':e['checkpoint'],'output':output})
        print(e['checkpoint']+': PASS',flush=True)
    elif e['checkpoint']=='final-release':
        run(['cmake','--preset','release',
             '-DFETCHCONTENT_SOURCE_DIR_GOOGLETEST='+str(REPO/'build/debug/_deps/googletest-src')])
        run(['cmake','--build','--preset','release','-j','4'])
        output=run(['ctest','--preset','release'])
        assert '0 tests failed out of 41' in output
        for name in ['xor','regression','scalar_autograd','mnist']:
            result=run([str(TEMP/'build/release'/name)],RECORDING)
            if name=='mnist':
                expected=baseline_output[baseline_output.index('Correct digit:'):].removesuffix('Success!\n')
                assert result==expected, 'MNIST output differs from baseline'
            RESULTS.append({'example':name,'output':result})
        print('Release tests and all four examples: PASS',flush=True)
        run(['cmake','--preset','sanitizers',
             '-DFETCHCONTENT_SOURCE_DIR_GOOGLETEST='+str(REPO/'build/debug/_deps/googletest-src')])
        run(['cmake','--build','--preset','sanitizers','-j','4'])
        output=run(['ctest','--preset','sanitizers'])
        assert '0 tests failed out of 41' in output
        RESULTS.append({'checkpoint':'sanitizers','output':output})
        print('Sanitizers: PASS',flush=True)

for path,text in files.items():
    assert text.rstrip()==(REPO/path).read_text().rstrip(),path+' differs from reviewed branch'
assert digest(RECORDING/'main.cpp')==original_hash
report={'baseline':'c9918e8','destination':run(['git','rev-parse','HEAD'],REPO).strip(),
        'edits':len(literal),'temporary_directory':str(TEMP),
        'recording_source_unchanged':True,'script_sha256':digest(HERE/'script.md'),
        'spoken_words':len(' '.join(x[2:] for x in script.splitlines() if x.startswith('> ')).split()),
        'results':RESULTS}
(HERE/'verification-run.json').write_text(json.dumps(report,indent=2)+'\n')
print('All edits replay; destination files match the review branch.',flush=True)
