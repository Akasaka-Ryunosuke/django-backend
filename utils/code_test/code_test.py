import os
import tempfile
import subprocess
import shutil
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 测试点根目录
TESTCASE_ROOT = 'utils/code_test/testcases'  # 请改为你的实际根目录

def submit_code(qid, code):
    """
    返回
      {
        "status": "accepted"|"wrong_answer"|"compile_error"|"timeout"|"runtime_error"|"error",
        "message"?: "...",
        "details"?: [...]
      }
    """
    # 2. 测试点目录
    base_dir = os.path.join(TESTCASE_ROOT, qid)
    if not os.path.isdir(base_dir):
        return JsonResponse({'status': 'error', 'message': '题目目录不存在'}, status=404)

    # 3. 扫描所有 .in 文件，并匹配 .out
    in_files = sorted(f for f in os.listdir(base_dir) if f.endswith('.in'))
    test_cases = []
    for in_file in in_files:
        name, _ = os.path.splitext(in_file)
        out_file = name + '.out'
        in_path = os.path.join(base_dir, in_file)
        out_path = os.path.join(base_dir, out_file)
        if not os.path.isfile(out_path):
            return JsonResponse({
                'status': 'error',
                'message': f'缺少输出文件：{out_file}'
            }, status=400)
        test_cases.append((in_path, out_path))

    # 4. 创建临时工作目录，写入源代码
    work_dir = tempfile.mkdtemp(prefix='judge_')
    src_path = os.path.join(work_dir, 'Main.c')    # 假设 C 语言
    exe_path = os.path.join(work_dir, 'Main.out')
    with open(src_path, 'w', encoding='utf-8') as f:
        f.write(code)

    # 5. 编译源代码
    cp = subprocess.run(
        ['gcc', src_path, '-o', exe_path],
        cwd=work_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if cp.returncode != 0:
        shutil.rmtree(work_dir)
        return JsonResponse({
            'status': 'compile_error',
            'message': cp.stderr
        })

    # 6. 逐个测试
    results = []
    overall = 'accepted'
    pass_num = 0
    for in_path, out_path in test_cases:
        try:
            proc = subprocess.run(
                [exe_path],
                cwd=work_dir,
                stdin=open(in_path, 'r', encoding='utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1,
                text=True
            )
        except subprocess.TimeoutExpired:
            overall = 'timeout'
            results.append({'case': os.path.basename(in_path), 'result': 'timeout'})
            break
        except Exception as e:
            overall = 'runtime_error'
            results.append({'case': os.path.basename(in_path), 'result': 'runtime_error', 'message': str(e)})
            break

        # 检查运行时错误
        if proc.returncode != 0:
            overall = 'runtime_error'
            results.append({'case': os.path.basename(in_path), 'result': 'runtime_error', 'message': proc.stderr})
            break

        # 读取标准输出并比较
        expected = open(out_path, 'r', encoding='utf-8').read().strip()
        actual = proc.stdout.strip()
        if actual != expected:
            overall = 'wrong_answer'
            results.append({
                'case': os.path.basename(in_path),
                'result': 'wrong_answer',
                'expected': expected,
                'actual': actual
            })
            break
        else:
            results.append({'case': os.path.basename(in_path), 'result': 'accepted'})
            pass_num += 1

    # 7. 清理临时目录
    shutil.rmtree(work_dir)

    # 8. 返回结果
    return {
        'status': overall,
        'details': results,
        'pass': pass_num,
        'all_test_size': len(test_cases)
    }


if __name__ == '__main__':
    code = '''
    #include <stdio.h>
int main()
{
    printf("Ad astra abyssosque !");
    return 0;
}
    '''
    print(submit_code('956A', code))
