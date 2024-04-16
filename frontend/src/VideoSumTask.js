import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import  ListItemText  from '@mui/material/ListItemText';

import VideoFile from '@mui/icons-material/VideoFile';

export const VideoSumTaskListItem = (
    <ListItemButton>
        <ListItemIcon>
            <VideoFile /> 
        </ListItemIcon>
        <ListItemText primary="Video Summarization"/>
    </ListItemButton>
);

export const VideoSumTaskResults = (
    <React.Fragment>

    </React.Fragment>
);