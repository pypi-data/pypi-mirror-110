from pipewire_python.controller import Controller

#########################
# PLAYBACK              #
#########################
# normal way
audio_controller = Controller(verbose=True)
audio_controller.Record(audio_filename='docs/5sec_record.wav',
                        timeout_seconds=5,
                        # Debug
                        verbose=True)
