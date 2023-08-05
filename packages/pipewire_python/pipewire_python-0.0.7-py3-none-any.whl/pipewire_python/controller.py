import asyncio
import json
import subprocess
import warnings

"""
[DOCS]:
- Asyncio https://docs.python.org/3/library/asyncio-subprocess.html
- Pipewire APIs https://www.linuxfromscratch.org/blfs/view/cvs/multimedia/pipewire.html
- APIs example https://fedoraproject.org/wiki/QA:Testcase_PipeWire_PipeWire_CLI

[NO ASYNC]:
    subprocess

[ASYNC]:
    asyncio
"""
MESSAGES_ERROR = {"NotImplementedError": "This function is not yet implemented",
                  "ValueError": "The value entered is wrong"}

RECOMMENDED_RATES = [8000, 11025, 16000, 22050, 44100,
                     48000, 88200, 96000, 176400, 192000, 352800, 384000]
RECOMMENDED_FORMATS = ["u8", "s8", "s16", "s32", "f32", "f64"]


# class Player():

#     commands_json = None

#     def __init__(self):

#         self.commands_json = PIPEWIRE_API_COMMANDS

#     def play_wav_file(self,
#                       # Test
#                       audio_path: str,
#                       # Debug
#                       verbose: bool = False
#                       ):
#         """
#         Execute pipewire command to play a WAV file

#         Args:
#             - audio_path (str): path of the file to be played.
#             Example: 'audios/my_audio.wav'
#         Return:
#             - shell_result (str): shell response to the command
#         """
#         warnings.warn('The name of the function may change on future releases', DeprecationWarning)

#         command = self.commands_json["play_default"]
#         if verbose:
#             print(command)
#         # Replace COMMAND_HERE to fill the command
#         command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
#                                                          command=command,
#                                                          replace_value=audio_path)
#         if verbose:
#             print(command_structure)
#         shell_subprocess = subprocess.Popen(command_structure,
#                                             stdout=subprocess.PIPE,
#                                             stderr=subprocess.STDOUT
#                                             )
#         stdout, stderr = shell_subprocess.communicate()
#         self._print_std(stdout, stderr, verbose=verbose)
#         return stdout, stderr

#     async def play_wav_file_async(self,
#                                   # Test
#                                   audio_path: str,
#                                   # Debug
#                                   verbose: bool = False
#                                   ):
#         """
#         [ASYNC] Execute pipewire command to play a WAV file

#         Args:
#             - audio_path (str): path of the file to be played.
#             Example: 'audios/my_audio.wav'
#         Return:
#             - shell_result (str): shell response to the command
#         """
#         warnings.warn('The name of the function may change on future releases', DeprecationWarning)

#         command = self.commands_json["play_default"]
#         if verbose:
#             print(command)
#         # Replace COMMAND_HERE to fill the command
#         command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
#                                                          command=command,
#                                                          replace_value=audio_path)
#         if verbose:
#             print(command_structure)
#         command_structure_joined = ' '.join(command_structure)
#         if verbose:
#             print(command_structure_joined)
#             _ = await asyncio.gather(self._run_shell_async('ls -l',
#                                                            verbose=verbose))
#         # PIPEWIRE Returns None when play command is used
#         _ = await asyncio.gather(self._run_shell_async(command_structure_joined,
#                                                        verbose=verbose))

#         return True

#     def record_wav_file(self,
#                         # Test
#                         audio_path: str,
#                         use_max_time: bool = True,
#                         seconds_to_record: int = 5,
#                         # Debug
#                         verbose: bool = False
#                         ):
#         """
#         Execute pipewire command to record a WAV file.
#         By default one second with all pipewire default
#         devices and properties selected.

#         Args:
#             - audio_path (str): path of the file to be played.
#             Example: 'audios/my_audio.wav'
#         Return:
#             - shell_result (str): shell response to the command
#         """
#         warnings.warn('The name of the function may change on future releases', DeprecationWarning)

#         command = self.commands_json["record_default"]
#         # Replace COMMAND_HERE to fill the command
#         command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
#                                                          command=command,
#                                                          replace_value=audio_path)
#         shell_subprocess = subprocess.Popen(command_structure,
#                                             stdout=subprocess.PIPE,
#                                             stderr=subprocess.STDOUT
#                                             )
#         try:
#             stdout, stderr = shell_subprocess.communicate(timeout=seconds_to_record)
#         except subprocess.TimeoutExpired as e:  # When script finish in time
#             shell_subprocess.kill()
#             stdout, stderr = shell_subprocess.communicate()

#         self._print_std(stdout, stderr, verbose=verbose)
#         return stdout, stderr

#     async def record_wav_file_async(self,
#                                     # Test
#                                     audio_path: str,
#                                     use_max_time: bool = True,
#                                     seconds_to_record: int = 5,
#                                     # Debug
#                                     verbose: bool = False
#                                     ):
#         """
#         [ASYNC] Execute pipewire command to record a WAV file.
#         By default one second with all pipewire default
#         devices and properties selected.

#         Args:
#             - audio_path (str): path of the file to be played.
#             Example: 'audios/my_audio.wav'
#         Return:
#             - shell_result (str): shell response to the command
#         """
#         raise NotImplementedError('This function is not yet implemmented.')
#         warnings.warn('The name of the function may change on future releases', DeprecationWarning)

#         command = self.commands_json["record_default"]
#         # Replace COMMAND_HERE to fill the command
#         command_structure = self._replace_key_by_command(key=KEY_TO_REPLACE,
#                                                          command=command,
#                                                          replace_value=audio_path)

#         if verbose:
#             print(command_structure)
#         command_structure_joined = ' '.join(command_structure)
#         if verbose:
#             print(command_structure_joined)
#             _ = await asyncio.gather(self._run_shell_async('ls -l',
#                                                            verbose=verbose))
#         # PIPEWIRE Returns None when play command is used
#         _ = await asyncio.gather(self._run_shell_async(command_structure_joined,
#                                                        verbose=verbose))

#         return True

#     async def _run_shell_async(self,
#                                # Test
#                                cmd: list,
#                                # Debug
#                                verbose: bool = False
#                                ):
#         """
#         [ASYNC] Function that execute shell commands in asyncio way

#         Args:
#             - cmd (str): command line to execute. Example: 'ls -l'
#         Return:
#             - shell_result (str): shell response to the command
#         """
#         proc = await asyncio.create_subprocess_shell(cmd,
#                                                      stdout=asyncio.subprocess.PIPE,
#                                                      stderr=asyncio.subprocess.PIPE)
#         stdout, stderr = await proc.communicate()
#         print(f'[{cmd!r} exited with {proc.returncode}]')
#         self._print_std(stdout, stderr, verbose=verbose)

#         return stdout, stderr

#     async def _run_shell_async_timeout(self,
#                                        timeout: int = 5,
#                                        ):
#         raise NotImplementedError('This function is not yet implemmented.')

#         try:
#             await asyncio.wait_for(print('Here the func'), timeout=timeout)
#         except asyncio.TimeoutError:
#             p.kill()
#             await p.communicate()

#     def _print_std(self,
#                    # Debug
#                    stdout: str,
#                    stderr: str,
#                    verbose: bool = False):

#         if (stdout != None and verbose == True):
#             print(f'[_print_std][stdout][type={type(stdout)}]\n{stdout.decode()}')
#         if (stderr != None and verbose == True):
#             print(f'[_print_std][stderr][type={type(stderr)}]\n{stderr.decode()}')

#     def _replace_key_by_command(self,
#                                 # Test
#                                 key: str = KEY_TO_REPLACE,
#                                 command: str = '',
#                                 replace_value: str = '',
#                                 # Debug
#                                 verbose: bool = False):
#         result = [item.replace(key, replace_value) for item in command]
#         print(f'[KEY /COMMAND /REPLACE_VALUE] -> RESULT IS [{result}]')
#         return result


class Controller():

    _pipewire_cli = {  # Help
        "--help": None,  # -h
        "--version": None,
        "--verbose": None,  # -v
        "--remote": None,  # -r
    }

    _pipewire_modes = {  # Modes
        "--playback": None,  # -p
        "--record": None,  # -r
        "--midi": None,  # -m
    }

    _pipewire_targets = {
        "--list-targets": None,
    }

    _pipewire_configs = {  # Configs
        "--media-type": None,  # *default=Audio
        "--media-category": None,  # *default=Playback
        "--media-role": None,  # *default=Music
        "--target": None,  # *default=auto
        # [100ns,100us, 100ms,100s] *default=100ms (SOURCE FILE if not specified)
        "--latency": None,
        # https://github.com/audiojs/sample-rate
        # [8000,11025,16000,22050,44100,48000,88200,96000,176400,192000,352800,384000] *default=48000
        "--rate": None,
        "--channels": None,  # [1,2] *default=2
        "--channel-map": None,  # ["stereo", "surround-51", "FL,FR"...] *default=unknown
        "--format": None,  # [u8|s8|s16|s32|f32|f64] *default=s16
        "--volume": None,  # [0.0,1.0] *default=1.000
        "--quality": None,  # -q # [0,15] *default=4
    }

    def __init__(self,
                 # Debug
                 verbose: bool = False
                 ):
        """
        Constructor that get default parameters of pipewire command line
        interface and assign to variables to use in python controller
        """
        # super().__init__()
        # LOAD ALL DEFAULT PARAMETERS

        mycommand = ['pw-cat', '-h']

        # get default parameters with help
        stdout, stderr = self._execute_shell_command(command=mycommand,
                                                     verbose=verbose
                                                     )
        # convert stdout to dictionary
        dict_default_values = self._get_dict_from_stdout(stdout=str(stdout.decode()),
                                                         verbose=verbose)

        if verbose:
            print(self._pipewire_configs)

        # Save default system configs to our json
        self._pipewire_configs.update(([(key, dict_default_values[key])
                                      for key in dict_default_values.keys()]))

        if verbose:
            print(self._pipewire_configs)

        # Delete keys with None values
        self._pipewire_configs = self._drop_keys_with_none_values(self._pipewire_configs)

        if verbose:
            print(self._pipewire_configs)

    def _help(self):
        """
        Get pipewire command line help
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def version(self):
        """
        Get version of pipewire installed on OS.
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def verbose(self):

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def set_config(self,
                   # configs
                   media_type: str = None,
                   media_category: str = None,
                   media_role: str = None,
                   target: str = None,
                   latency: str = None,
                   rate: int = None,
                   channels: int = None,
                   channels_map: str = None,
                   _format: str = None,
                   volume: float = None,
                   quality: int = None,
                   # Debug
                   verbose: bool = False,
                   ):
        """
        Set configuration to playback or record with pw-cat command.
        """
        # 1 - media_type
        if media_type:
            self._pipewire_configs["--media-type"] = str(media_type)
        elif media_type == None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[media_type='{media_type}'] EMPTY VALUE")
        # 2 - media_category
        if media_category:
            self._pipewire_configs["--media-category"] = str(media_category)
        elif media_category == None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[media_category='{media_category}'] EMPTY VALUE")
        # 3 - media_role
        if media_role:
            self._pipewire_configs["--media-role"] = str(media_role)
        elif media_role == None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[media_role='{media_role}'] EMPTY VALUE")
        # 4 - target
        if target:
            self._pipewire_configs["--target"] = str(target)
        elif target == None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[target='{target}'] EMPTY VALUE")
        # 5 - latency
        if latency:
            if any(chr.isdigit() for chr in latency):  # Contain numbers
                self._pipewire_configs["--latency"] = str(latency)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[latency='{latency}'] NO NUMBER IN VARIABLE")
        elif latency == None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[latency='{latency}'] EMPTY VALUE")
        # 6 - rate
        if rate:
            if rate in RECOMMENDED_RATES:
                self._pipewire_configs["--rate"] = str(rate)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[rate='{rate}'] VALUE NOT IN RECOMMENDED LIST \n{RECOMMENDED_RATES}")
        elif rate == None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[rate='{rate}'] EMPTY VALUE")
        # 7 - channels
        if channels:
            if channels in [1, 2]:  # values
                self._pipewire_configs["--channels"] = str(channels)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[channels='{channels}'] WRONG VALUE\n ONLY 1 or 2.")
        elif channels == None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[channels='{channels}'] EMPTY VALUE")
        # 8 - channels-map
        if channels_map:
            self._pipewire_configs["--channels-map"] = str(channels_map)
        elif channels_map == None:
            pass
        else:
            raise ValueError(
                f"{MESSAGES_ERROR['ValueError']}[channels_map='{channels_map}'] EMPTY VALUE")
        # 9 - format
        if _format:
            if _format in RECOMMENDED_FORMATS:
                self._pipewire_configs["--format"] = str(_format)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[_format='{_format}'] VALUE NOT IN RECOMMENDED LIST \n{RECOMMENDED_FORMATS}")
        elif _format == None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[_format='{_format}'] EMPTY VALUE")
        # 10 - volume
        if volume:
            if 0.0 <= volume <= 1.0:
                self._pipewire_configs["--volume"] = str(volume)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[volume='{volume}'] OUT OF RANGE \n [0.000, 1.000]")
        elif volume == None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[volume='{volume}'] EMPTY VALUE")
        # 11 - quality
        if quality:
            if 0 <= quality <= 15:
                self._pipewire_configs["--quality"] = str(quality)
            else:
                raise ValueError(
                    f"{MESSAGES_ERROR['ValueError']}[quality='{quality}'] OUT OF RANGE \n [0, 15]")
        elif quality == None:
            pass
        else:
            raise ValueError(f"{MESSAGES_ERROR['ValueError']}[volume='{volume}'] EMPTY VALUE")

        if verbose:
            print(self._pipewire_configs)

    def list_targets(self,
                     mode,  # playback or record
                     ):
        """
        Returns a list of targets to playback or record. Then you can use
        the output to select a device to playback or record.
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def Playback(self,
                 audio_filename: str = 'myplayback.wav',
                 # Debug
                 verbose: bool = False
                 ):
        """
        Execute pipewire command to play an audio file

        Args:
            - audio_filename (str): path of the file to be played. *default='myplayback.wav'
        Return:
            - stdout (str): shell response to the command
            - stderr (str): shell response to the command
        """
        warnings.warn('The name of the function may change on future releases', DeprecationWarning)

        mycommand = ['pw-cat', '--playback', audio_filename]+self._generate_command_by_dict(dict=self._pipewire_configs,
                                                                                            verbose=verbose)

        if verbose:
            print(f'[mycommand]{mycommand}')

        stdout, stderr = self._execute_shell_command(command=mycommand,
                                                     timeout=-1,
                                                     verbose=verbose)
        return stdout, stderr

    def Record(self,
               audio_filename: str = 'myplayback.wav',
               timeout_seconds=5,
               # Debug
               verbose: bool = False
               ):
        """
        Execute pipewire command to record an audio file

        Args:
            - audio_filename (str): path of the file to be played. *default='myplayback.wav'
        Return:
            - stdout (str): shell response to the command
            - stderr (str): shell response to the command
        """
        warnings.warn('The name of the function may change on future releases', DeprecationWarning)

        mycommand = ['pw-cat', '--record', audio_filename]+self._generate_command_by_dict(dict=self._pipewire_configs,
                                                                                            verbose=verbose)

        if verbose:
            print(f'[mycommand]{mycommand}')

        stdout, stderr = self._execute_shell_command(command=mycommand,
                                                     timeout=timeout_seconds,
                                                     verbose=verbose)
        return stdout, stderr

    def clear_devices(self,
                      mode: str = 'all',  # ['all','playback','record']
                      # Debug
                      verbose: bool = False,
                      ):
        """
        Function to stop process running under pipewire.
        Example: pw-cat process
        """

        raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def _execute_shell_command(self,
                               command: str,
                               timeout: int = -1,  # *default= no limit
                               # Debug
                               verbose: bool = False,
                               ):
        """
        Execute command on terminal via subprocess

        Args:
            - command (str): command line to execute. Example: 'ls -l'
            - timeout (int): (seconds) time to end the terminal process
            # Debug
            - verbose (bool): print variables for debug purposes
        Return:
            - stdout (str): terminal response to the command
            - stderr (str): terminal response to the command
        """
        # Create subprocess
        terminal_subprocess = subprocess.Popen(command,  # Example ['ls ','l']
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.STDOUT
                                               )
        # Execute command depending or not in timeout
        try:
            if timeout == -1:
                stdout, stderr = terminal_subprocess.communicate()
            else:
                stdout, stderr = terminal_subprocess.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:  # When script finish in time
            terminal_subprocess.kill()
            stdout, stderr = terminal_subprocess.communicate()

        # Print terminal output
        self._print_std(stdout,
                        stderr,
                        verbose=verbose)

        # Return terminal output
        return stdout, stderr

    async def _execute_shell_command_async(self,
                                           command: list,
                                           timeout: int = -1,
                                           # Debug
                                           verbose: bool = False
                                           ):
        """
        [ASYNC] Function that execute terminal commands in asyncio way

        Args:
            - command (str): command line to execute. Example: 'ls -l'
        Return:
            - stdout (str): terminal response to the command
            - stderr (str): terminal response to the command
        """
        if timeout == -1:
            # No timeout
            terminal_process_async = await asyncio.create_subprocess_shell(command,
                                                                           stdout=asyncio.subprocess.PIPE,
                                                                           stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await terminal_process_async.communicate()
            print(f'[_execute_shell_command_async]\
                    [{command!r} exited with\
                    {terminal_process_async.returncode}]')
            self._print_std(stdout,
                            stderr,
                            verbose=verbose)

            return stdout, stderr

        else:
            raise NotImplementedError(MESSAGES_ERROR['NotImplementedError'])

    def _print_std(self,
                   # Debug
                   stdout: str,
                   stderr: str,
                   verbose: bool = False):
        """
        Print terminal output if are different to None and verbose activated
        """

        if (stdout != None and verbose == True):
            print(f'[_print_std][stdout][type={type(stdout)}]\n{stdout.decode()}')
        if (stderr != None and verbose == True):
            print(f'[_print_std][stderr][type={type(stderr)}]\n{stderr.decode()}')

    def _get_dict_from_stdout(self,
                              stdout: str,
                              # Debug
                              verbose: bool = False,
                              ):

        rows = stdout.split('\n')
        config_dict = {}
        for row in rows:
            if 'default' in row:
                key = '--'+row.split('--')[1].split(' ')[0]
                value = row.split('default ')[1].replace(')', '')
                config_dict[key] = value
        if verbose:
            print(config_dict)
        return config_dict

    def _update_dict_by_dict(self,
                             main_dict: dict,
                             secondary_dict: dict,
                             ):
        return main_dict.update(([(key, secondary_dict[key]) for key in secondary_dict.keys()]))

    def _drop_keys_with_none_values(self,
                                    main_dict: dict):
        return {k: v for k, v in main_dict.items() if v is not None}

    def _generate_command_by_dict(self,
                                  dict: dict,
                                  # Debug
                                  verbose: bool = False
                                  ):
        array_command = []
        # append to a list
        [array_command.extend([k, v]) for k, v in dict.items()]
        # return values
        return array_command
