import aiofiles
import aiohttp
import asyncio
import io
import os
import zipfile
from typing import Optional, Tuple, Union

async def download_file(url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"下载失败，状态码: {response.status}")
                return await response.text()
    except Exception as e:
        print(f"下载文件错误: {str(e)}")
        raise e

def get_sort_key(channel_name: str) -> tuple:
    if 'CCTV5+' in channel_name:
        return (1, 5.5, [], '')

    numbers = []
    letters = []
    current_number = ''
    
    for char in channel_name:
        if char.isdigit():
            current_number += char
        else:
            if current_number:
                numbers.append(int(current_number))
                current_number = ''
            if char.isalpha():
                letters.append(char.lower())
    
    if current_number:
        numbers.append(int(current_number))

    priority = 999
    name_lower = channel_name.lower()
    
    if 'cctv' in name_lower:
        priority = 1
    elif '卫视' in name_lower:
        priority = 2
    elif 'cgtn' in name_lower:
        priority = 3
    elif any(x in name_lower for x in ['凤凰', 'tvb', '香港', '澳门']):
        priority = 4
    elif any(x in name_lower for x in ['民视', '中视', '华视', '台视']):
        priority = 5
        
    # 4. 返回排序元组
    return (
        priority,
        numbers[0] if numbers else float('inf'),
        numbers[1:],
        ''.join(letters)
    )

async def process_and_save(content: str, filename: str, base_dir: Optional[str] = None) -> str:
    try:
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        file_path = os.path.join(base_dir, filename)

        channels = {}
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or ',' not in line:
                continue
                
            channel_name, url = line.split(',', 1)
            category = get_channel_category(channel_name)
            
            if category not in channels:
                channels[category] = []
            if (channel_name, url) not in channels[category]:
                channels[category].append((channel_name, url))

        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:

            for category in sorted(channels.keys()):
                await f.write(f"{category},#genre#\n")

                sorted_channels = sorted(channels[category], 
                                      key=lambda x: get_sort_key(x[0]))
                
                for channel_name, url in sorted_channels:
                    await f.write(f"{channel_name},{url}\n")
                await f.write("\n")
                
        return file_path
    except Exception as e:
        print(f"处理和保存文件错误: {str(e)}")
        raise e

def get_channel_category(channel_name: str) -> str:
    """根据频道名称返回对应分类"""
    if 'CCTV' in channel_name or '央视' in channel_name:
        return '央视频道'
    elif '卫视' in channel_name:
        return '卫视频道'
    elif 'CGTN' in channel_name:
        return 'CGTN频道'
    elif any(name in channel_name for name in ['凤凰', 'TVB', '香港', '澳门', '台湾']):
        return '港澳台频道'
    elif any(name in channel_name for name in ['RTHK', 'HOY']):
        return '香港频道'
    elif '澳视' in channel_name:
        return '澳门频道'
    elif any(name in channel_name for name in ['民视', '中视', '华视', '台视', 'TVBS']):
        return '台湾频道'
    else:
        return '其他频道'

async def download_zip(url: str) -> bytes:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"下载失败，状态码: {response.status}")
                return await response.read()
    except Exception as e:
        print(f"下载zip文件错误: {str(e)}")
        raise e

def extract_zip(zip_content: bytes, extract_filename: str = None, password: Optional[bytes] = None) -> Tuple[str, bytes]:
    try:
        zip_data = io.BytesIO(zip_content)
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            filename = extract_filename if extract_filename in file_list else file_list[0]
            content = zip_ref.read(filename, pwd=password)
            return filename, content
    except Exception as e:
        print(f"解压文件错误: {str(e)}")
        raise e

async def write_file(content: bytes, filename: str, base_dir: Optional[str] = None) -> str:

    try:
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        file_path = os.path.join(base_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        return file_path
    except Exception as e:
        print(f"写入文件错误: {str(e)}")
        raise e

async def getname(name):
    print(f"正在获取{name}的直播源...")
    try:
        if 'iptv' in name:
            zip_content = await download_zip("http://api.y977.com/iptv.txt.zip")
            _, iptv_content = extract_zip(
                zip_content,
                extract_filename="iptv.txt",
                password=b'xfflchVCWG9941'
            )
            iptv_path = await write_file(iptv_content, name)
            print(f"IPTV文件已保存到: {iptv_path}")
            
        else:
            return name
            
    except Exception as e:
        print(f"获取直播源错误: {str(e)}")
        return name

async def main():
    await getname("iptv.txt")

if __name__ == "__main__":
    asyncio.run(main())