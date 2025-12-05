import re
import random

def shuffle_options(match):
    line = match.group(0)
    
    opts_match = re.search(r'opts:\s*\[(.*?)\]', line, re.DOTALL)
    
    if not opts_match:
        return line
    
    try:
        opts_str = opts_match.group(1)
        opts = re.findall(r'"([^"]*)"', opts_str)
        
        if len(opts) < 2:
            return line
        
        # الخيار الأول دائماً هو الإجابة الصحيحة
        correct_answer = opts[0]
        other_opts = opts[1:]
        
        # خلط جميع الخيارات
        all_opts = [correct_answer] + other_opts
        random.shuffle(all_opts)
        
        # بناء الخيارات الجديدة
        new_opts_str = ', '.join(f'"{opt}"' for opt in all_opts)
        new_line = line[:opts_match.start(1)] + new_opts_str + line[opts_match.end(1):]
        
        return new_line
    except Exception as e:
        print(f'خطأ: {e}')
        return line

files = ['chapter01.html', 'chapter02.html', 'chapter3_fixed.html', 'chapter4_fixed.html']

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'const questions = [' not in content:
            print(f'⚠️ {file_path}: لا توجد مصفوفة questions')
            continue
        
        start = content.find('const questions = [')
        end = content.find('];', start) + 2
        questions_str = content[start:end]
        
        # البحث عن كل سؤال وتطبيق التبديل
        new_questions = re.sub(r'\{[^{}]*?\}', shuffle_options, questions_str, flags=re.DOTALL)
        
        new_content = content[:start] + new_questions + content[end:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ {file_path}: تم التحديث بنجاح')
    
    except Exception as e:
        print(f'❌ {file_path}: خطأ - {e}')

print('\n✅ اكتمل!')

