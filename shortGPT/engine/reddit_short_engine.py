    def _editAndRenderShort(self):
        """
        Override parent method to customize video rendering sequence by adding a Reddit image
        """
        self.verifyParameters(
            voiceover_audio_url=self._db_audio_path,
            video_duration=self._db_background_video_duration,
            music_url=self._db_background_music_url
        )

        outputPath = self.dynamicAssetDir + "rendered_video.mp4"
        if not os.path.exists(outputPath):
            self.logger("Rendering short: Starting automated editing...")
            videoEditor = EditingEngine()
            videoEditor.addEditingStep(EditingStep.ADD_VOICEOVER_AUDIO, {'url': self._db_audio_path})
            videoEditor.addEditingStep(EditingStep.ADD_BACKGROUND_MUSIC, {
                'url': self._db_background_music_url,
                'loop_background_music': self._db_voiceover_duration,
                "volume_percentage": 0.11
            })
            videoEditor.addEditingStep(EditingStep.CROP_1920x1080, {'url': self._db_background_trimmed})
            videoEditor.addEditingStep(EditingStep.ADD_SUBSCRIBE_ANIMATION, {'url': AssetDatabase.get_asset_link('subscribe animation')})

            if self._db_watermark:
                videoEditor.addEditingStep(EditingStep.ADD_WATERMARK, {'text': self._db_watermark})
            
            videoEditor.addEditingStep(EditingStep.ADD_REDDIT_IMAGE, {'url': self._db_reddit_thread_image})
            
            caption_type = EditingStep.ADD_CAPTION_SHORT_ARABIC if self._db_language == Language.ARABIC.value else EditingStep.ADD_CAPTION_SHORT
            
            if isinstance(self._db_timed_captions, list):
                for item in self._db_timed_captions:
                    if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], tuple) and len(item[0]) == 2:
                        timing, text = item
                        videoEditor.addEditingStep(caption_type, {
                            'text': text.upper(),
                            'set_time_start': timing[0],
                            'set_time_end': timing[1]
                        })
                    else:
                        self.logger(f"WARNING: Skipping invalid caption format -> {item}")

            if self._db_num_images:
                for item in self._db_timed_image_urls:
                    if isinstance(item, tuple) and len(item) == 2:
                        timing, image_url = item
                        videoEditor.addEditingStep(EditingStep.SHOW_IMAGE, {
                            'url': image_url,
                            'set_time_start': timing[0],
                            'set_time_end': timing[1]
                        })
                    else:
                        self.logger(f"WARNING: Skipping invalid image format -> {item}")

            videoEditor.renderVideo(outputPath, logger=self.logger if self.logger is not self.default_logger else None)
        
        self._db_video_path = outputPath
