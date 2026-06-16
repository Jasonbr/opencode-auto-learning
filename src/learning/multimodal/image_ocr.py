#!/usr/bin/env python3
"""
图片 OCR 模块
提取图片中的文字并保存为记忆
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import hashlib
import base64

class ImageOCR:
    """图片 OCR 处理器"""
    
    def __init__(self, user_id="default"):
        self.user_id = user_id
        self.mem0_db = Path.home() / ".mem0" / "local_memory.db"
        self.storage_dir = Path.home() / ".mem0" / "images"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def process_image(self, image_path: str, description: str = "") -> Dict:
        """处理图片并提取文字"""
        image_path = Path(image_path)
        
        if not image_path.exists():
            return {"error": "Image not found", "path": str(image_path)}
        
        # 生成唯一 ID
        image_id = hashlib.md5(str(image_path).encode()).hexdigest()[:12]
        
        # 保存图片副本
        stored_path = self._store_image(image_path, image_id)
        
        # 尝试 OCR
        text_content = self._extract_text(image_path)
        
        # 生成描述
        if not description:
            description = self._generate_description(text_content)
        
        # 保存到数据库
        memory_id = self._save_to_memory(image_id, text_content, description, stored_path)
        
        return {
            "image_id": image_id,
            "memory_id": memory_id,
            "text_content": text_content[:500] if text_content else "",
            "description": description,
            "stored_path": str(stored_path),
            "has_text": bool(text_content)
        }
    
    def _store_image(self, image_path: Path, image_id: str) -> Path:
        """存储图片副本"""
        ext = image_path.suffix.lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
            ext = '.png'
        
        stored_name = f"{image_id}{ext}"
        stored_path = self.storage_dir / stored_name
        
        # 复制图片
        import shutil
        shutil.copy2(image_path, stored_path)
        
        return stored_path
    
    def _extract_text(self, image_path: Path) -> Optional[str]:
        """提取图片中的文字"""
        try:
            # 尝试使用 pytesseract
            from PIL import Image
            import pytesseract
            
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            return text.strip()
        except ImportError:
            # 如果没有安装，返回提示
            return "[OCR not available - install pytesseract to extract text]"
        except Exception as e:
            return f"[OCR error: {str(e)}]"
    
    def _generate_description(self, text_content: str) -> str:
        """生成图片描述"""
        if not text_content:
            return "Image without extractable text"
        
        # 提取前 100 个字符作为描述
        preview = text_content[:100].replace('\n', ' ')
        return f"Image containing: {preview}..."
    
    def _save_to_memory(self, image_id: str, text_content: str, description: str, stored_path: Path) -> int:
        """保存到记忆数据库"""
        if not self.mem0_db.exists():
            return -1
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        content = f"[IMAGE] {description}\n\nExtracted text:\n{text_content[:1000] if text_content else 'N/A'}"
        
        cursor.execute("""
            INSERT INTO memories (user_id, content, category, metadata, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.user_id,
            content,
            "multimodal",
            json.dumps({
                "type": "image",
                "image_id": image_id,
                "stored_path": str(stored_path),
                "has_text": bool(text_content),
                "text_length": len(text_content) if text_content else 0
            }),
            datetime.now().isoformat()
        ))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return memory_id
    
    def search_images(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索图片记忆"""
        if not self.mem0_db.exists():
            return []
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, content, metadata, created_at
            FROM memories
            WHERE category = 'multimodal'
            AND (content LIKE ? OR metadata LIKE ?)
            ORDER BY created_at DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit))
        
        results = []
        for row in cursor.fetchall():
            metadata = json.loads(row[2]) if row[2] else {}
            results.append({
                "id": row[0],
                "content": row[1][:200],
                "metadata": metadata,
                "created_at": row[3]
            })
        
        conn.close()
        return results

def main():
    import sys
    
    ocr = ImageOCR()
    
    if len(sys.argv) < 2:
        print("Usage: image_ocr.py <image_path> [description]")
        print("Example: image_ocr.py screenshot.png \"Architecture diagram\"")
        return
    
    image_path = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(f"Processing image: {image_path}")
    result = ocr.process_image(image_path, description)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
