from pipewire_python.controller import Controller

#########################
# PLAYBACK              #
#########################
# normal way
audio_controller = Controller(verbose=True)
audio_controller.set_config(rate=384000,
                            channels=2,
                            _format='f64',
                            volume=0.98,
                            quality=4,
                            # Debug
                            verbose=True)
audio_controller.Playback(audio_filename='docs/beers.wav',
                          # Debug
                          verbose=True)