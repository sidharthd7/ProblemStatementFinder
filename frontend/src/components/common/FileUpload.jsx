import { useRef, useState } from 'react';

export default function FileUpload({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (isValidFile(file)) {
      onUpload(file);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (isValidFile(file)) {
      onUpload(file);
    }
  };

  const isValidFile = (file) => {
    if (!file) return false;
    const validExtensions = ['.xlsx', '.xls'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    return validExtensions.includes(fileExtension);
  };

  return (
    <div
      className={`relative border-2 border-dashed rounded-lg p-4 text-center cursor-pointer
        ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
        hover:border-blue-500 transition-colors duration-200`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
    >
      <input
        type="file"
        ref={fileInputRef}
        className="hidden"
        accept=".xlsx,.xls"
        onChange={handleFileSelect}
      />
      <div className="space-y-2">
        <div className="text-gray-600">
          Upload Problem Statement File
        </div>
        <div className="text-sm text-gray-500">
          (.xlsx format)
        </div>
      </div>
    </div>
  );
}