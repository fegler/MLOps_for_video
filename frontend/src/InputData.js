import IconButton from "@mui/material/IconButton";
import PhotoCamera from '@mui/icons-material/PhotoCamera';
import FileUpload from '@mui/icons-material/FileUpload';
import { useEffect, useState } from "react";
import axios from 'axios';

export const InputData = () => {
    const [selectedFile, setSelectedFile] = useState()
    const [preview, setPreview] = useState()

    useEffect(() => {
        if (!selectedFile) {
            setPreview(undefined)
            return
        }

        const objectUrl = URL.createObjectURL(selectedFile)
        setPreview(objectUrl)

        return () => URL.revokeObjectURL(objectUrl)
    }, [selectedFile])

    const onSelectFile = e => {
        if (!e.target.files || e.target.files.length === 0) {
            setSelectedFile(undefined)
            return
        }
        setSelectedFile(e.target.files[0])
    }

    const onSubmitClick = e => {
        if (!selectedFile) return
        const formData = new FormData();
        formData.append("file", selectedFile)
        axios
            .post("http://localhost:8000/image_upload", formData)
            .then((res) => {
                alert("File Upload success")
            })
            .catch((err) => alert("File Upload Error"))
    }

    return (
        <>
            <input
                accept="image/*"
                onChange={onSelectFile}
                id="icon-button-photo"
                type="file"
                style={{ display: 'none' }}
                multiple="multiple"
            />
            {!selectedFile && <label htmlFor="icon-button-photo">
                <IconButton color="primary" component="span">
                    <FileUpload fontSize="large" />
                </IconButton>
            </label>}
            {selectedFile && <img src={preview} style={{ width: '80%', height: '80%' }} />}
            <button onClick={onSubmitClick}>Submit</button>
        </>
    );
};
