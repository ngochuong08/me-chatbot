"""
Document Compare - So sánh các phiên bản tài liệu
"""

import difflib
from typing import Dict, List, Tuple
from document_processor import DocumentProcessor


class DocumentCompare:
    def __init__(self):
        self.processor = DocumentProcessor()
    
    def compare_documents(
        self, 
        file_path1: str, 
        file_path2: str
    ) -> Dict:
        """So sánh 2 documents và trả về differences"""
        
        # Load full text from both documents
        text1 = self.processor.get_document_text(file_path1)
        text2 = self.processor.get_document_text(file_path2)
        
        # Split into lines for comparison
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        # Get differences
        diff = difflib.unified_diff(
            lines1, 
            lines2, 
            lineterm='',
            fromfile=file_path1,
            tofile=file_path2
        )
        
        diff_text = '\n'.join(diff)
        
        # Get detailed comparison
        matcher = difflib.SequenceMatcher(None, text1, text2)
        similarity_ratio = matcher.ratio()
        
        # Get changed blocks
        changes = self._get_changes(lines1, lines2)
        
        return {
            "file1": file_path1,
            "file2": file_path2,
            "similarity": f"{similarity_ratio * 100:.2f}%",
            "diff": diff_text,
            "changes": changes,
            "summary": self._generate_summary(changes, similarity_ratio)
        }
    
    def _get_changes(
        self, 
        lines1: List[str], 
        lines2: List[str]
    ) -> Dict:
        """Lấy chi tiết các thay đổi"""
        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))
        
        added = []
        removed = []
        modified = []
        
        for line in diff:
            if line.startswith('+ '):
                added.append(line[2:])
            elif line.startswith('- '):
                removed.append(line[2:])
            elif line.startswith('? '):
                continue
        
        return {
            "added_lines": len(added),
            "removed_lines": len(removed),
            "added_content": added[:10],  # First 10 changes
            "removed_content": removed[:10]
        }
    
    def _generate_summary(
        self, 
        changes: Dict, 
        similarity: float
    ) -> str:
        """Tạo summary về sự khác biệt"""
        summary = []
        
        summary.append(f"📊 Độ tương đồng: {similarity * 100:.2f}%")
        summary.append(f"➕ Số dòng thêm mới: {changes['added_lines']}")
        summary.append(f"➖ Số dòng bị xóa: {changes['removed_lines']}")
        
        if changes['added_lines'] == 0 and changes['removed_lines'] == 0:
            summary.append("\n✅ Hai tài liệu giống hệt nhau")
        elif similarity > 0.9:
            summary.append("\n✅ Hai tài liệu rất giống nhau, chỉ có thay đổi nhỏ")
        elif similarity > 0.7:
            summary.append("\n⚠️ Hai tài liệu có một số thay đổi đáng kể")
        else:
            summary.append("\n❗ Hai tài liệu có nhiều khác biệt lớn")
        
        return "\n".join(summary)
    
    def compare_text(self, text1: str, text2: str) -> Dict:
        """So sánh 2 đoạn text trực tiếp"""
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        matcher = difflib.SequenceMatcher(None, text1, text2)
        similarity_ratio = matcher.ratio()
        
        changes = self._get_changes(lines1, lines2)
        
        return {
            "similarity": f"{similarity_ratio * 100:.2f}%",
            "changes": changes,
            "summary": self._generate_summary(changes, similarity_ratio)
        }
    
    def get_html_diff(self, text1: str, text2: str) -> str:
        """Tạo HTML diff để hiển thị trên web"""
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        html_diff = difflib.HtmlDiff()
        html = html_diff.make_file(
            lines1, 
            lines2,
            fromdesc="Version 1",
            todesc="Version 2",
            context=True,
            numlines=3
        )
        
        return html


if __name__ == "__main__":
    # Test
    comparer = DocumentCompare()
    
    # Example: compare two text strings
    text1 = """
    Quy định nghỉ phép năm 2023:
    - Nhân viên dưới 1 năm: 12 ngày
    - Nhân viên từ 1-5 năm: 15 ngày
    - Nhân viên trên 5 năm: 18 ngày
    """
    
    text2 = """
    Quy định nghỉ phép năm 2024:
    - Nhân viên dưới 1 năm: 12 ngày
    - Nhân viên từ 1-5 năm: 16 ngày
    - Nhân viên trên 5 năm: 20 ngày
    - Nhân viên trên 10 năm: 22 ngày
    """
    
    result = comparer.compare_text(text1, text2)
    print("Comparison Result:")
    print(result['summary'])
    print(f"\nChanges: {result['changes']}")
