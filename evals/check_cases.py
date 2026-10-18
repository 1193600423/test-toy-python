"""Check public case metadata and reproduction against immutable baseline commits."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

REPO = Path(__file__).resolve().parents[1]


def main():
    paths = sorted((REPO / 'evals/cases').glob('*/case.json'))
    assert len(paths) == 3, 'expected three development cases'
    for path in paths:
        case = json.loads(path.read_text())
        assert case['case_id'] == path.parent.name
        assert case['acceptance_criteria'] and case['constraints']
        json.loads((path.parent / case['environment']['spec']).read_text())
        with tempfile.TemporaryDirectory(prefix='toy-public-case-') as directory:
            workspace = Path(directory)
            archive = subprocess.run(['git', '-C', str(REPO), 'archive', case['repository']['base_commit']], check=True, capture_output=True, timeout=30).stdout
            with tarfile.open(fileobj=io.BytesIO(archive)) as source:
                source.extractall(workspace, filter='data')
            original = workspace / case['issue']['source_path']
            assert hashlib.sha256(original.read_bytes()).hexdigest() == case['issue']['sha256']
            assert original.read_bytes() == (path.parent / case['issue']['snapshot']).read_bytes()
            assert hashlib.sha256((workspace / 'uv.lock').read_bytes()).hexdigest() == case['environment']['lockfile_sha256']
            environment = {key: os.environ[key] for key in ('PATH', 'HOME', 'TMPDIR', 'SYSTEMROOT') if key in os.environ}
            environment.update(PYTHONPATH=str(workspace / 'src'), PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run([sys.executable, str(path.parent / case['reproduction']['script'])], cwd=workspace, env=environment, capture_output=True, text=True, timeout=case['reproduction']['timeout_seconds'])
            assert result.returncode == case['reproduction']['expected_before_exit_code'], result.stderr
            assert 'AssertionError' in result.stderr, result.stderr
            assert case['reproduction']['observed_before'] in result.stdout, result.stdout
            print(f"{case['case_id']}: metadata valid; baseline reproduced")


if __name__ == '__main__':
    main()
