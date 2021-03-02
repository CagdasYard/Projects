classdef Spectrogram < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        Spectogram                      matlab.ui.Figure
        TabGroup2                       matlab.ui.container.TabGroup
        DataAcquisitionTab              matlab.ui.container.Tab
        UseasoundfileButtonGroup        matlab.ui.container.ButtonGroup
        RecordButton                    matlab.ui.control.RadioButton
        UploadSoundButton               matlab.ui.control.RadioButton
        SamplingRateHzKnobLabel         matlab.ui.control.Label
        SamplingRateHzKnob              matlab.ui.control.DiscreteKnob
        StartRecordingButton            matlab.ui.control.Button
        StopRecordingButton             matlab.ui.control.Button
        PlayButton                      matlab.ui.control.Button
        OpenButton                      matlab.ui.control.Button
        AcquiredSignal                  matlab.ui.control.UIAxes
        DataGenerationTab               matlab.ui.container.Tab
        GenerateasignalPanel            matlab.ui.container.Panel
        TabGroup                        matlab.ui.container.TabGroup
        SinusoidalTab                   matlab.ui.container.Tab
        PhaseLabel                      matlab.ui.control.Label
        SinusoidPhase                   matlab.ui.control.Spinner
        FrequencyHzLabel                matlab.ui.control.Label
        SinusoidFrequency               matlab.ui.control.Spinner
        AmplitudeSpinner_4Label         matlab.ui.control.Label
        SinusoidAmplitude               matlab.ui.control.Spinner
        GenerateSinusoidalButton        matlab.ui.control.Button
        SquareTab                       matlab.ui.container.Tab
        PhaseSpinner_6Label             matlab.ui.control.Label
        SquarePhase                     matlab.ui.control.Spinner
        FrequencyHzLabel_2              matlab.ui.control.Label
        SquareFrequency                 matlab.ui.control.Spinner
        AmplitudeSpinner_6Label         matlab.ui.control.Label
        SquareAmplitude                 matlab.ui.control.Spinner
        GenerateSquare                  matlab.ui.control.Button
        DutyCycleLabel                  matlab.ui.control.Label
        SquareDutyCycle                 matlab.ui.control.Spinner
        SawtoothTab                     matlab.ui.container.Tab
        PhaseSpinner_5Label             matlab.ui.control.Label
        SawtoothPhase                   matlab.ui.control.Spinner
        AmplitudeSpinner_5Label         matlab.ui.control.Label
        SawtoothAmplitude               matlab.ui.control.Spinner
        FrequencyHzLabel_3              matlab.ui.control.Label
        SawtoothFrequency               matlab.ui.control.Spinner
        GenerateSawtooth                matlab.ui.control.Button
        WidthSpinnerLabel               matlab.ui.control.Label
        SawtoothWidth                   matlab.ui.control.Spinner
        WindowedSinusoidalTab           matlab.ui.container.Tab
        WindowFunctionButtonGroup       matlab.ui.container.ButtonGroup
        ChooseButton                    matlab.ui.control.RadioButton
        UseButton                       matlab.ui.control.RadioButton
        OpenButton_2                    matlab.ui.control.Button
        ListBoxLabel                    matlab.ui.control.Label
        WindowList                      matlab.ui.control.ListBox
        WindowdurationsSpinnerLabel     matlab.ui.control.Label
        WindowDuration                  matlab.ui.control.Spinner
        AmplitudeSpinner_2Label         matlab.ui.control.Label
        WindowedSinusoidalAmplitude     matlab.ui.control.Spinner
        FrequencyHzLabel_4              matlab.ui.control.Label
        WindowedSinusoidalFrequency     matlab.ui.control.Spinner
        PhaseLabel_3                    matlab.ui.control.Label
        WindowedSinusoidalPhase         matlab.ui.control.Spinner
        GenerateWindowedSinusoidal      matlab.ui.control.Button
        StartingtimesLabel              matlab.ui.control.Label
        StartTime                       matlab.ui.control.Spinner
        RectangleWindowedLinearChirpTab  matlab.ui.container.Tab
        PhaseLabel_2                    matlab.ui.control.Label
        LinearChirpPhase                matlab.ui.control.Spinner
        BandwidthHzLabel                matlab.ui.control.Label
        LinearChirpBandwidth            matlab.ui.control.Spinner
        AmplitudeSpinner_7Label         matlab.ui.control.Label
        LinearChirpAmplitude            matlab.ui.control.Spinner
        GenerateLinearChirp             matlab.ui.control.Button
        InitialinstantenousfrequencyHzLabel  matlab.ui.control.Label
        LinearChirpInitial              matlab.ui.control.Spinner
        DurationSpinnerLabel            matlab.ui.control.Label
        LinearChirpDuration             matlab.ui.control.Spinner
        TimeshiftSpinnerLabel           matlab.ui.control.Label
        LinearChirpTimeshift            matlab.ui.control.Spinner
        MultipleSinusoidalTab           matlab.ui.container.Tab
        MultipleSinusoidalTable         matlab.ui.control.Table
        AddButton                       matlab.ui.control.Button
        RemoveButton                    matlab.ui.control.Button
        GenerateMultipleSinusoidal      matlab.ui.control.Button
        SamplingfrequencyHzSpinnerLabel  matlab.ui.control.Label
        SamplingfrequencyHzSpinner      matlab.ui.control.Spinner
        DurationsSpinnerLabel           matlab.ui.control.Label
        DurationsSpinner                matlab.ui.control.Spinner
        GeneratedSignalTimeDomain       matlab.ui.control.UIAxes
        GeneratedSignalFrequencyDomain  matlab.ui.control.UIAxes
        SpectrogramTab                  matlab.ui.container.Tab
        InputSignalButtonGroup          matlab.ui.container.ButtonGroup
        UseacquiredsignalButton         matlab.ui.control.RadioButton
        UsegeneratedsignalButton        matlab.ui.control.RadioButton
        WindowSignalPanel               matlab.ui.container.Panel
        WindowTypeLabel                 matlab.ui.control.Label
        WindowList_2                    matlab.ui.control.ListBox
        WindowSampleSizeLabel           matlab.ui.control.Label
        WindowSampleSizeSpinner         matlab.ui.control.Spinner
        WindowOverlapSpinnerLabel       matlab.ui.control.Label
        WindowOverlapSpinner            matlab.ui.control.Spinner
        PlotButton                      matlab.ui.control.Button
        SpectrogramPlot                 matlab.ui.control.UIAxes
    end


    properties (Access = public)
        recObj;
        AcquiredSignalVar;
        FsKnob;
        FsAcquired;
        GeneratedSignalVar;
        uploadwindow;
    end

    methods (Access = private)
    
        function AcquiredSignalPlot(app, Fs)
            t = (0:numel(app.AcquiredSignalVar)-1) / Fs;
            plot(app.AcquiredSignal,t,app.AcquiredSignalVar);
            app.AcquiredSignal.XLim = [t(1) t(end)];
        end

        function GeneratedSignalTimeDomainPlot(app)
            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            d = app.DurationsSpinner.Value;
            t = 0:1/generatedFs:d - 1/generatedFs;
            plot(app.GeneratedSignalTimeDomain,t,app.GeneratedSignalVar);
            app.GeneratedSignalTimeDomain.XLim = [t(1) t(end)];

            app.WindowSampleSizeSpinner.Limits = [0 numel(app.GeneratedSignalVar)];
            app.WindowOverlapSpinner.Limits = [0 numel(app.GeneratedSignalVar) - 1];
            app.InputSignalButtonGroup.SelectedObject = app.UsegeneratedsignalButton;
            app.PlotButton.Enable = 'on';

        end
        function GeneratedSignalFreqDomainPlot(app)
            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            length = numel(app.GeneratedSignalVar);
            fftSignal = fft(app.GeneratedSignalVar,length);
            fftSignal = fftshift(fftSignal);
            f = ((-1:2/length:1-2/length)*generatedFs/2);
            
            plot(app.GeneratedSignalFrequencyDomain,f,abs(fftSignal) / length);
            app.GeneratedSignalFrequencyDomain.XLim = [f(1) f(end)];
        end
        function SpectrogramPlotFunc(app)
            
            selectedButton = app.InputSignalButtonGroup.SelectedObject;
            selectedButton2 = app.UseasoundfileButtonGroup.SelectedObject;
            
            switch selectedButton
                case app.UseacquiredsignalButton
                    x = transpose(app.AcquiredSignalVar);
                    
                    switch selectedButton2
                        case app.RecordButton
                            Fs = app.FsKnob;                       
                        case app.UploadSoundButton
                            Fs = app.FsAcquired;                             
                    end
                    
                case app.UsegeneratedsignalButton        
                    x = app.GeneratedSignalVar;
                    Fs = app.SamplingfrequencyHzSpinner.Value;
            end
            
            Overlap = app.WindowOverlapSpinner.Value;
            WindowSampleSize = app.WindowSampleSizeSpinner.Value;
            FunctionNameCell = {'Barthann', 'Bartlett', 'Blackman',...
                'Blackman - Harris', 'Bohman', 'Chebyshev', 'Flat Top',...
                'Gaussian', 'Hamming', 'Hann', 'Kaiser', 'Nuttall', 'Parzen',...
                'Rectangular', 'Taylor', 'Triangular', 'Tukey'};
            
            FunctionHandleCell = {@(t) barthannwin(t), @(t) bartlett(t),...
                @(t) blackman(t), @(t) blackmanharris(t), @(t) bohmanwin(t),...
                @(t) chebwin(t), @(t) flattopwin(t), @(t) gausswin(t),...
                @(t) hamming(t), @(t) hann(t), @(t) kaiser(t), @(t) nuttallwin(t),...
                @(t) parzenwin(t), @(t) rectwin(t), @(t) taylorwin(t),...
                @(t) triang(t), @(t) tukeywin(t)};
                
            FunctionHandleMap = containers.Map(FunctionNameCell,FunctionHandleCell);

            WindowName = app.WindowList_2.Value;
            WindowFunction = FunctionHandleMap(WindowName);
            H = WindowFunction(WindowSampleSize);
            
            Sizex = numel(x);
            SizeH = numel(H);
            f = transpose(linspace(0,Fs,20));
            
            PartitionCount = fix((Sizex - SizeH)/(SizeH - Overlap));
            LB = 1:(SizeH - Overlap):1+(SizeH - Overlap) * PartitionCount;
            UB = SizeH:(SizeH - Overlap): PartitionCount * (SizeH - Overlap) + SizeH;
            
            XPartition = mat2cell([LB;UB]',ones(size(LB)),2);
            XPartition = cellfun(@(M) x(M(1):M(2)),XPartition,'UniformOutput',false);
            XPartition = cell2mat(XPartition);
            
            E = exp(-1i*2*pi*f*(0:numel(H)-1)/Fs);
            
            STFT = XPartition * (repmat(H,[1,numel(f)]) .* E');
            DB = transpose(10*log10(eps + abs(flip(STFT))));

            tsc = 0:1/Fs:(numel(x)-1)/Fs;
            IM = imagesc(app.SpectrogramPlot,flip(tsc),flip(f),DB);
            
            app.SpectrogramPlot.YLim = [IM.YData(end) IM.YData(1)];     
            app.SpectrogramPlot.XLim = [IM.XData(end) IM.XData(1)];
            app.SpectrogramPlot.YDir = 'normal';
            Colorbar = colorbar(app.SpectrogramPlot);
            Colorbar.Label.String = 'Power/frequency (dB/Hz)';
            app.SpectrogramPlot.FontSize = 10;
        end      
    end


    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app)
               
            app.FsKnob = 44100;    
            app.FsAcquired = 44100;
            app.PlayButton.Enable = 'off';
            
            app.GeneratedSignalFrequencyDomain.XLim = [-1 1];
            
            app.AcquiredSignal.Title.String  = 'Signal';
            app.AcquiredSignal.XLabel.String = 't';
            app.AcquiredSignal.YLabel.String = 'x(t)';
            
            app.MultipleSinusoidalTable.Data = [0,0,0];
        end

        % Button pushed function: StartRecordingButton
        function StartRecordingButtonPushed(app, ~)
            nBits = 16; 
            nChannels = 1; 
            app.PlayButton.Enable = 'off';
            app.StopRecordingButton.Enable = 'on';
            app.SamplingRateHzKnob.Enable = 'off';
            
            app.recObj = audiorecorder(app.FsAcquired, nBits, nChannels); %create audio object
            record(app.recObj); %start Recording 
                
        end

        % Button pushed function: StopRecordingButton
        function StopRecordingButtonPushed(app, ~)
            stop(app.recObj) % Stop audio recording   
            app.AcquiredSignalVar=getaudiodata(app.recObj);
           
            AcquiredSignalPlot(app,app.FsKnob)

            app.StopRecordingButton.Enable = 'off';
            app.SamplingRateHzKnob.Enable = 'on';
            app.PlayButton.Enable = 'on';
            
            app.WindowSampleSizeSpinner.Limits = [0 numel(app.AcquiredSignalVar)];
            app.WindowOverlapSpinner.Limits = [0 numel(app.AcquiredSignalVar) - 1];
            app.InputSignalButtonGroup.SelectedObject = app.UseacquiredsignalButton;
            app.PlotButton.Enable = 'on';
            
            
        end

        % Button pushed function: OpenButton
        function OpenButtonPushed(app, ~)
            [file,path] = uigetfile({'*.wav';'*.mp3';'*.mp4'});
            
            if ~isequal(path,0)
                [app.AcquiredSignalVar,app.FsAcquired] = audioread(fullfile(path,file));
                app.SamplingRateHzKnob.Value = num2str(app.FsAcquired);
                app.PlayButton.Enable = 'on';
                AcquiredSignalPlot(app,app.FsAcquired)
                
                app.WindowSampleSizeSpinner.Limits = [0 numel(app.AcquiredSignalVar)];
                app.WindowOverlapSpinner.Limits = [0 numel(app.AcquiredSignalVar) - 1];
                app.InputSignalButtonGroup.SelectedObject = app.UseacquiredsignalButton;
                app.PlotButton.Enable = 'on';

            end
            
            
        end

        % Button pushed function: PlayButton
        function PlayButtonPushed(app, ~)
            selectedButton = app.UseasoundfileButtonGroup.SelectedObject;
            
            switch selectedButton
                case app.RecordButton
                    Fs = app.FsKnob;

                case app.UploadSoundButton
                    Fs = app.FsAcquired;                    
            end
            sound(app.AcquiredSignalVar,Fs,16);
        end

        % Value changed function: SamplingRateHzKnob
        function SamplingRateHzKnobValueChanged(app, ~)
            app.FsKnob = str2num(app.SamplingRateHzKnob.Value);
            if ~isempty(app.AcquiredSignalVar)
                AcquiredSignalPlot(app,app.FsKnob)
            end
        end

        % Button pushed function: OpenButton_2
        function OpenButton_2Pushed(app, ~)
            
            [file,path] = uigetfile('*.mat');
           
            if ~isequal(path,0)
                S = load(fullfile(path,file));

                if isa(S,'struct')
                    C = struct2cell(S);
                    app.uploadwindow = cell2mat(C);
                else
                    app.uploadwindow = S;
                end
                app.GenerateWindowedSinusoidal.Enable = 'on';
            else
            app.GenerateWindowedSinusoidal.Enable = 'off';    
            end
            

        end

        % Selection changed function: WindowFunctionButtonGroup
        function WindowFunctionButtonGroupSelectionChanged(app, ~)
            selectedButton = app.WindowFunctionButtonGroup.SelectedObject;
            
            switch selectedButton
                case app.ChooseButton
                    app.WindowDuration.Enable = 'on';
                    app.StartTime.Enable = 'on';
                    app.WindowList.Enable = 'on';
                    app.OpenButton_2.Enable = 'off';
                    app.GenerateWindowedSinusoidal.Enable = 'on';
                    
                case app.UseButton
                    app.WindowDuration.Enable = 'off';
                    app.StartTime.Enable = 'off';
                    app.WindowList.Enable = 'off';                    
                    app.OpenButton_2.Enable = 'on';
                    
                    if isempty(app.uploadwindow)
                        app.GenerateWindowedSinusoidal.Enable = 'off';
                    end
            end
        end

        % Button pushed function: AddButton
        function AddButtonPushed(app, ~)
            app.MultipleSinusoidalTable.Data = [app.MultipleSinusoidalTable.Data;0,0,0];
        end

        % Button pushed function: RemoveButton
        function RemoveButtonPushed(app, ~)
            app.MultipleSinusoidalTable.Data = app.MultipleSinusoidalTable.Data(1:end-1,:);            
        end

        % Button pushed function: GenerateSinusoidalButton
        function GenerateSinusoidalButtonPushed(app, ~)
            A = app.SinusoidAmplitude.Value;
            f = app.SinusoidFrequency.Value;
            theta = pi * app.SinusoidPhase.Value / 180;
            
            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            d = app.DurationsSpinner.Value;
            t = 0:1/generatedFs:d - 1/generatedFs;
            
            Sinusoidal = @(t,A,f,theta) A*cos(2*pi*f*t + theta);
            
            app.GeneratedSignalVar = Sinusoidal(t,A,f,theta);
            GeneratedSignalTimeDomainPlot(app);
            GeneratedSignalFreqDomainPlot(app);
        end

        % Button pushed function: GenerateSawtooth
        function GenerateSawtoothPushed(app, ~)
            A = app.SawtoothAmplitude.Value;
            f = app.SawtoothFrequency.Value;
            theta = app.SawtoothPhase.Value;
            width = app.SawtoothWidth.Value;  

            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            d = app.DurationsSpinner.Value;            
            t = -theta:1/generatedFs:d -theta - 1/generatedFs;
            
            app.GeneratedSignalVar = A * sawtooth(2*pi*f*t,width);
            GeneratedSignalTimeDomainPlot(app);
            GeneratedSignalFreqDomainPlot(app);
        end

        % Button pushed function: GenerateWindowedSinusoidal
        function GenerateWindowedSinusoidalButtonPushed(app, ~)
            A = app.WindowedSinusoidalAmplitude.Value;
            f = app.WindowedSinusoidalFrequency.Value;
            theta = pi * app.WindowedSinusoidalPhase.Value / 180;
            
            selectedButton = app.WindowFunctionButtonGroup.SelectedObject;
            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            d = app.DurationsSpinner.Value;            
            
            FunctionNameCell = {'Barthann', 'Bartlett', 'Blackman',...
                'Blackman - Harris', 'Bohman', 'Chebyshev', 'Flat Top',...
                'Gaussian', 'Hamming', 'Hann', 'Kaiser', 'Nuttall', 'Parzen',...
                'Rectangular', 'Taylor', 'Triangular', 'Tukey'};
            
            FunctionHandleCell = {@(t) barthannwin(t), @(t) bartlett(t),...
                @(t) blackman(t), @(t) blackmanharris(t), @(t) bohmanwin(t),...
                @(t) chebwin(t), @(t) flattopwin(t), @(t) gausswin(t),...
                @(t) hamming(t), @(t) hann(t), @(t) kaiser(t), @(t) nuttallwin(t),...
                @(t) parzenwin(t), @(t) rectwin(t), @(t) taylorwin(t),...
                @(t) triang(t), @(t) tukeywin(t)};
                
            FunctionHandleMap = containers.Map(FunctionNameCell,FunctionHandleCell);  
            wd = app.WindowDuration.Value;
            s = app.StartTime.Value;
            
            t = 0:1/generatedFs:d - 1/generatedFs;
            t1= 0:1/generatedFs:wd - 1/generatedFs;
            
            switch selectedButton
                case app.ChooseButton
                    WindowName = app.WindowList.Value;
                    WindowFunction = FunctionHandleMap(WindowName);
                    Window = transpose(WindowFunction(numel(t1)));
                    
                    if numel(t1) <= numel(t)
                       Window = [Window, zeros(1,numel(t)-numel(Window))];
                    else
                       Window = Window(1:numel(t));
                    end   
                    
                    app.GeneratedSignalVar = A * cos(2*pi*f*(t+s) + theta) .* Window;
                    GeneratedSignalTimeDomainPlot(app);
                    GeneratedSignalFreqDomainPlot(app);
                    
                case app.UseButton
                    Window = app.uploadwindow;

                    if numel(Window) <= numel(t)
                       Window = [Window  zeros(1,numel(t)-numel(Window))];
                    else
                       Window = Window(1:numel(t));
                    end   
                    
                    app.GeneratedSignalVar = A * cos(2*pi*f*(t+s) + theta) .* transpose(Window);
                    GeneratedSignalTimeDomainPlot(app);
                    GeneratedSignalFreqDomainPlot(app);
            end   
                 
        end

        % Button pushed function: GenerateLinearChirp
        function GenerateLinearChirpButtonPushed(app, ~)
            f0 = app.LinearChirpInitial.Value;
            theta = pi * app.LinearChirpPhase.Value / 180;
            BW = app.LinearChirpBandwidth.Value;
            A = app.LinearChirpAmplitude.Value;
            dchirp = app.LinearChirpDuration.Value;
            t0 = app.LinearChirpTimeshift.Value;
            
            Chirp = @(t,A,f0,BW,d,theta) ...
                    A * cos(2*pi*(f0*t + BW * (t.^2) / (2*d) ) + theta ) .* (0 <= t) .* (t < d);
                
            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            d = app.DurationsSpinner.Value;            
            t = -t0:1/generatedFs:d -t0 - 1/generatedFs;

            app.GeneratedSignalVar = Chirp(t,A,f0,BW,dchirp,theta);
            GeneratedSignalTimeDomainPlot(app);
            GeneratedSignalFreqDomainPlot(app);
            
        end

        % Button pushed function: GenerateSquare
        function GenerateSquareButtonPushed(app, ~)
            A = app.SquareAmplitude.Value;
            f = app.SquareFrequency.Value;
            theta = app.SquarePhase.Value;
            Duty = app.SquareDutyCycle.Value;
            
            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            d = app.DurationsSpinner.Value;
            t = 0:1/generatedFs:d - 1/generatedFs;
            
            Square= @(t,A,f,Duty,Phase) A * (0 <= mod(t-Phase,1/f)) .* (mod(t-Phase,1/f)< Duty/(100*f)) ;
            
            app.GeneratedSignalVar = Square(t,A,f,Duty,theta);
            GeneratedSignalTimeDomainPlot(app);
            GeneratedSignalFreqDomainPlot(app);
            
        end

        % Button pushed function: GenerateMultipleSinusoidal
        function GenerateMultipleSinusoidalButtonPushed(app, ~)
            Sinusoidal = @(t,A,f,theta)A*cos(2*pi*f*t+(pi*theta/180));
            
            M = app.MultipleSinusoidalTable.Data;
            Cell = mat2cell(M,ones(size(M,1),1),3);
            
            generatedFs = app.SamplingfrequencyHzSpinner.Value;
            d = app.DurationsSpinner.Value;
            t = 0:1/generatedFs:d - 1/generatedFs;
            
            Cell = cellfun(@(C) Sinusoidal(t,C(1),C(2),C(3)), Cell,'UniformOutput',false);
            M = cell2mat(Cell);
            if size(M,1) > 1
                app.GeneratedSignalVar = sum(M);
            else
                app.GeneratedSignalVar = M;
            end
            GeneratedSignalTimeDomainPlot(app);
            GeneratedSignalFreqDomainPlot(app);
            
        end

        % Selection changed function: UseasoundfileButtonGroup
        function UseasoundfileButtonGroupSelectionChanged(app, ~)
            selectedButton = app.UseasoundfileButtonGroup.SelectedObject;
            
            switch selectedButton
                case app.RecordButton
                    app.OpenButton.Enable = 'off';
                    app.StartRecordingButton.Enable = 'on';
                    app.StopRecordingButton.Enable = 'on';                    
                    app.SamplingRateHzKnob.Enable = 'on';
                
                case app.UploadSoundButton
                    app.OpenButton.Enable = 'on';
                    app.StartRecordingButton.Enable = 'off';
                    app.StopRecordingButton.Enable = 'off';
                    app.SamplingRateHzKnob.Enable = 'off';
                    
            end
        end

        % Selection changed function: InputSignalButtonGroup
        function InputSignalButtonGroupSelectionChanged(app, ~)
            selectedButton = app.InputSignalButtonGroup.SelectedObject;

            switch selectedButton                
                case app.UseacquiredsignalButton
                    if isempty(app.AcquiredSignalVar)
                    app.PlotButton.Enable = 'off';
                    else 
                    app.PlotButton.Enable = 'on';
                    app.WindowSampleSizeSpinner.Limits = [0 numel(app.AcquiredSignalVar)];
                    app.WindowOverlapSpinner.Limits = [0 numel(app.AcquiredSignalVar) - 1];                    
                    end
                case app.UsegeneratedsignalButton                   
                    if isempty(app.GeneratedSignalVar)
                    app.PlotButton.Enable = 'off';
                    else 
                    app.PlotButton.Enable = 'on';    
                    app.WindowSampleSizeSpinner.Limits = [0 numel(app.GeneratedSignalVar)];
                    app.WindowOverlapSpinner.Limits = [0 numel(app.GeneratedSignalVar) - 1];
                    end
            end
        end

        % Button pushed function: PlotButton
        function PlotButtonPushed(app, ~)
            SpectrogramPlotFunc(app);
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create Spectogram and hide until all components are created
            app.Spectogram = uifigure('Visible', 'off');
            app.Spectogram.AutoResizeChildren = 'off';
            app.Spectogram.Position = [100 100 952 639];
            app.Spectogram.Name = 'Spectrogram';
            app.Spectogram.Resize = 'off';

            % Create TabGroup2
            app.TabGroup2 = uitabgroup(app.Spectogram);
            app.TabGroup2.AutoResizeChildren = 'off';
            app.TabGroup2.Position = [1 1 952 639];

            % Create DataAcquisitionTab
            app.DataAcquisitionTab = uitab(app.TabGroup2);
            app.DataAcquisitionTab.AutoResizeChildren = 'off';
            app.DataAcquisitionTab.Title = 'Data Acquisition';

            % Create UseasoundfileButtonGroup
            app.UseasoundfileButtonGroup = uibuttongroup(app.DataAcquisitionTab);
            app.UseasoundfileButtonGroup.AutoResizeChildren = 'off';
            app.UseasoundfileButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @UseasoundfileButtonGroupSelectionChanged, true);
            app.UseasoundfileButtonGroup.Title = 'Use a sound file';
            app.UseasoundfileButtonGroup.Position = [66 260 288 302];

            % Create RecordButton
            app.RecordButton = uiradiobutton(app.UseasoundfileButtonGroup);
            app.RecordButton.Text = 'Record your sound';
            app.RecordButton.Position = [11 256 126 15];
            app.RecordButton.Value = true;

            % Create UploadSoundButton
            app.UploadSoundButton = uiradiobutton(app.UseasoundfileButtonGroup);
            app.UploadSoundButton.Text = 'Upload a sound file';
            app.UploadSoundButton.Position = [11 71 128 15];

            % Create SamplingRateHzKnobLabel
            app.SamplingRateHzKnobLabel = uilabel(app.UseasoundfileButtonGroup);
            app.SamplingRateHzKnobLabel.HorizontalAlignment = 'center';
            app.SamplingRateHzKnobLabel.VerticalAlignment = 'top';
            app.SamplingRateHzKnobLabel.Position = [32 130 112 15];
            app.SamplingRateHzKnobLabel.Text = 'Sampling Rate (Hz)';

            % Create SamplingRateHzKnob
            app.SamplingRateHzKnob = uiknob(app.UseasoundfileButtonGroup, 'discrete');
            app.SamplingRateHzKnob.Items = {'8000', '11025', '22050', '44100', '48000', '96000'};
            app.SamplingRateHzKnob.ValueChangedFcn = createCallbackFcn(app, @SamplingRateHzKnobValueChanged, true);
            app.SamplingRateHzKnob.Position = [58 160 60 60];
            app.SamplingRateHzKnob.Value = '44100';

            % Create StartRecordingButton
            app.StartRecordingButton = uibutton(app.UseasoundfileButtonGroup, 'push');
            app.StartRecordingButton.ButtonPushedFcn = createCallbackFcn(app, @StartRecordingButtonPushed, true);
            app.StartRecordingButton.Position = [178 216 100 22];
            app.StartRecordingButton.Text = 'Start Recording';

            % Create StopRecordingButton
            app.StopRecordingButton = uibutton(app.UseasoundfileButtonGroup, 'push');
            app.StopRecordingButton.ButtonPushedFcn = createCallbackFcn(app, @StopRecordingButtonPushed, true);
            app.StopRecordingButton.Enable = 'off';
            app.StopRecordingButton.Position = [178 179 100 22];
            app.StopRecordingButton.Text = 'Stop Recording';

            % Create PlayButton
            app.PlayButton = uibutton(app.UseasoundfileButtonGroup, 'push');
            app.PlayButton.ButtonPushedFcn = createCallbackFcn(app, @PlayButtonPushed, true);
            app.PlayButton.Position = [178 15 100 22];
            app.PlayButton.Text = 'Play';

            % Create OpenButton
            app.OpenButton = uibutton(app.UseasoundfileButtonGroup, 'push');
            app.OpenButton.ButtonPushedFcn = createCallbackFcn(app, @OpenButtonPushed, true);
            app.OpenButton.Enable = 'off';
            app.OpenButton.Position = [178 67 100 22];
            app.OpenButton.Text = 'Open';

            % Create AcquiredSignal
            app.AcquiredSignal = uiaxes(app.DataAcquisitionTab);
            title(app.AcquiredSignal, 'Audio Signal')
            xlabel(app.AcquiredSignal, 't')
            ylabel(app.AcquiredSignal, 'x(t)')
            app.AcquiredSignal.XGrid = 'on';
            app.AcquiredSignal.YGrid = 'on';
            app.AcquiredSignal.Box = 'on';
            app.AcquiredSignal.Position = [445 260 364 302];

            % Create DataGenerationTab
            app.DataGenerationTab = uitab(app.TabGroup2);
            app.DataGenerationTab.AutoResizeChildren = 'off';
            app.DataGenerationTab.Title = 'Data Generation';

            % Create GenerateasignalPanel
            app.GenerateasignalPanel = uipanel(app.DataGenerationTab);
            app.GenerateasignalPanel.AutoResizeChildren = 'off';
            app.GenerateasignalPanel.TitlePosition = 'centertop';
            app.GenerateasignalPanel.Title = 'Generate a signal';
            app.GenerateasignalPanel.Position = [10 212 510 380];

            % Create TabGroup
            app.TabGroup = uitabgroup(app.GenerateasignalPanel);
            app.TabGroup.AutoResizeChildren = 'off';
            app.TabGroup.Position = [1 0 510 360];

            % Create SinusoidalTab
            app.SinusoidalTab = uitab(app.TabGroup);
            app.SinusoidalTab.AutoResizeChildren = 'off';
            app.SinusoidalTab.Title = 'Sinusoidal';

            % Create PhaseLabel
            app.PhaseLabel = uilabel(app.SinusoidalTab);
            app.PhaseLabel.HorizontalAlignment = 'right';
            app.PhaseLabel.VerticalAlignment = 'top';
            app.PhaseLabel.Position = [25 136 56 15];
            app.PhaseLabel.Text = 'Phase (°)';

            % Create SinusoidPhase
            app.SinusoidPhase = uispinner(app.SinusoidalTab);
            app.SinusoidPhase.Position = [96 132 100 22];

            % Create FrequencyHzLabel
            app.FrequencyHzLabel = uilabel(app.SinusoidalTab);
            app.FrequencyHzLabel.HorizontalAlignment = 'center';
            app.FrequencyHzLabel.VerticalAlignment = 'top';
            app.FrequencyHzLabel.Position = [18 190 66 28];
            app.FrequencyHzLabel.Text = {'Frequency '; '(Hz)'};

            % Create SinusoidFrequency
            app.SinusoidFrequency = uispinner(app.SinusoidalTab);
            app.SinusoidFrequency.Limits = [0 Inf];
            app.SinusoidFrequency.Position = [96 193 100 22];

            % Create AmplitudeSpinner_4Label
            app.AmplitudeSpinner_4Label = uilabel(app.SinusoidalTab);
            app.AmplitudeSpinner_4Label.HorizontalAlignment = 'right';
            app.AmplitudeSpinner_4Label.VerticalAlignment = 'top';
            app.AmplitudeSpinner_4Label.Position = [21 253 60 15];
            app.AmplitudeSpinner_4Label.Text = 'Amplitude';

            % Create SinusoidAmplitude
            app.SinusoidAmplitude = uispinner(app.SinusoidalTab);
            app.SinusoidAmplitude.Position = [96 249 100 22];

            % Create GenerateSinusoidalButton
            app.GenerateSinusoidalButton = uibutton(app.SinusoidalTab, 'push');
            app.GenerateSinusoidalButton.ButtonPushedFcn = createCallbackFcn(app, @GenerateSinusoidalButtonPushed, true);
            app.GenerateSinusoidalButton.Position = [375 24 100 22];
            app.GenerateSinusoidalButton.Text = 'Generate';

            % Create SquareTab
            app.SquareTab = uitab(app.TabGroup);
            app.SquareTab.AutoResizeChildren = 'off';
            app.SquareTab.Title = 'Square';

            % Create PhaseSpinner_6Label
            app.PhaseSpinner_6Label = uilabel(app.SquareTab);
            app.PhaseSpinner_6Label.HorizontalAlignment = 'right';
            app.PhaseSpinner_6Label.VerticalAlignment = 'top';
            app.PhaseSpinner_6Label.Position = [41 136 40 15];
            app.PhaseSpinner_6Label.Text = 'Phase';

            % Create SquarePhase
            app.SquarePhase = uispinner(app.SquareTab);
            app.SquarePhase.Position = [96 132 100 22];

            % Create FrequencyHzLabel_2
            app.FrequencyHzLabel_2 = uilabel(app.SquareTab);
            app.FrequencyHzLabel_2.HorizontalAlignment = 'center';
            app.FrequencyHzLabel_2.VerticalAlignment = 'top';
            app.FrequencyHzLabel_2.Position = [18 190 66 28];
            app.FrequencyHzLabel_2.Text = {'Frequency '; '(Hz)'};

            % Create SquareFrequency
            app.SquareFrequency = uispinner(app.SquareTab);
            app.SquareFrequency.Limits = [0 Inf];
            app.SquareFrequency.Position = [96 193 100 22];

            % Create AmplitudeSpinner_6Label
            app.AmplitudeSpinner_6Label = uilabel(app.SquareTab);
            app.AmplitudeSpinner_6Label.HorizontalAlignment = 'right';
            app.AmplitudeSpinner_6Label.VerticalAlignment = 'top';
            app.AmplitudeSpinner_6Label.Position = [21 253 60 15];
            app.AmplitudeSpinner_6Label.Text = 'Amplitude';

            % Create SquareAmplitude
            app.SquareAmplitude = uispinner(app.SquareTab);
            app.SquareAmplitude.Position = [96 249 100 22];

            % Create GenerateSquare
            app.GenerateSquare = uibutton(app.SquareTab, 'push');
            app.GenerateSquare.ButtonPushedFcn = createCallbackFcn(app, @GenerateSquareButtonPushed, true);
            app.GenerateSquare.Position = [375 24 100 22];
            app.GenerateSquare.Text = 'Generate';

            % Create DutyCycleLabel
            app.DutyCycleLabel = uilabel(app.SquareTab);
            app.DutyCycleLabel.HorizontalAlignment = 'right';
            app.DutyCycleLabel.VerticalAlignment = 'top';
            app.DutyCycleLabel.Position = [274 253 86 15];
            app.DutyCycleLabel.Text = 'Duty Cycle (%)';

            % Create SquareDutyCycle
            app.SquareDutyCycle = uispinner(app.SquareTab);
            app.SquareDutyCycle.Limits = [0 100];
            app.SquareDutyCycle.Position = [375 249 100 22];

            % Create SawtoothTab
            app.SawtoothTab = uitab(app.TabGroup);
            app.SawtoothTab.AutoResizeChildren = 'off';
            app.SawtoothTab.Title = 'Sawtooth';

            % Create PhaseSpinner_5Label
            app.PhaseSpinner_5Label = uilabel(app.SawtoothTab);
            app.PhaseSpinner_5Label.HorizontalAlignment = 'right';
            app.PhaseSpinner_5Label.VerticalAlignment = 'top';
            app.PhaseSpinner_5Label.Position = [41 136 40 15];
            app.PhaseSpinner_5Label.Text = 'Phase';

            % Create SawtoothPhase
            app.SawtoothPhase = uispinner(app.SawtoothTab);
            app.SawtoothPhase.Position = [96 132 100 22];

            % Create AmplitudeSpinner_5Label
            app.AmplitudeSpinner_5Label = uilabel(app.SawtoothTab);
            app.AmplitudeSpinner_5Label.HorizontalAlignment = 'right';
            app.AmplitudeSpinner_5Label.VerticalAlignment = 'top';
            app.AmplitudeSpinner_5Label.Position = [21 253 60 15];
            app.AmplitudeSpinner_5Label.Text = 'Amplitude';

            % Create SawtoothAmplitude
            app.SawtoothAmplitude = uispinner(app.SawtoothTab);
            app.SawtoothAmplitude.Position = [96 249 100 22];

            % Create FrequencyHzLabel_3
            app.FrequencyHzLabel_3 = uilabel(app.SawtoothTab);
            app.FrequencyHzLabel_3.HorizontalAlignment = 'center';
            app.FrequencyHzLabel_3.VerticalAlignment = 'top';
            app.FrequencyHzLabel_3.Position = [18 190 66 28];
            app.FrequencyHzLabel_3.Text = {'Frequency '; '(Hz)'};

            % Create SawtoothFrequency
            app.SawtoothFrequency = uispinner(app.SawtoothTab);
            app.SawtoothFrequency.Limits = [0 Inf];
            app.SawtoothFrequency.Position = [96 193 100 22];

            % Create GenerateSawtooth
            app.GenerateSawtooth = uibutton(app.SawtoothTab, 'push');
            app.GenerateSawtooth.ButtonPushedFcn = createCallbackFcn(app, @GenerateSawtoothPushed, true);
            app.GenerateSawtooth.Position = [375 24 100 22];
            app.GenerateSawtooth.Text = 'Generate';

            % Create WidthSpinnerLabel
            app.WidthSpinnerLabel = uilabel(app.SawtoothTab);
            app.WidthSpinnerLabel.HorizontalAlignment = 'right';
            app.WidthSpinnerLabel.VerticalAlignment = 'top';
            app.WidthSpinnerLabel.Position = [324 253 36 15];
            app.WidthSpinnerLabel.Text = 'Width';

            % Create SawtoothWidth
            app.SawtoothWidth = uispinner(app.SawtoothTab);
            app.SawtoothWidth.Step = 0.1;
            app.SawtoothWidth.Limits = [0 1];
            app.SawtoothWidth.Position = [375 249 100 22];

            % Create WindowedSinusoidalTab
            app.WindowedSinusoidalTab = uitab(app.TabGroup);
            app.WindowedSinusoidalTab.AutoResizeChildren = 'off';
            app.WindowedSinusoidalTab.Title = 'Windowed Sinusoidal';

            % Create WindowFunctionButtonGroup
            app.WindowFunctionButtonGroup = uibuttongroup(app.WindowedSinusoidalTab);
            app.WindowFunctionButtonGroup.AutoResizeChildren = 'off';
            app.WindowFunctionButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @WindowFunctionButtonGroupSelectionChanged, true);
            app.WindowFunctionButtonGroup.Title = 'Window Function';
            app.WindowFunctionButtonGroup.Position = [212 113 282 203];

            % Create ChooseButton
            app.ChooseButton = uiradiobutton(app.WindowFunctionButtonGroup);
            app.ChooseButton.Text = {'Choose a'; 'window function'};
            app.ChooseButton.Position = [11 144 110 28];
            app.ChooseButton.Value = true;

            % Create UseButton
            app.UseButton = uiradiobutton(app.WindowFunctionButtonGroup);
            app.UseButton.Text = 'Or use your own';
            app.UseButton.Position = [10 23 111 15];

            % Create OpenButton_2
            app.OpenButton_2 = uibutton(app.WindowFunctionButtonGroup, 'push');
            app.OpenButton_2.ButtonPushedFcn = createCallbackFcn(app, @OpenButton_2Pushed, true);
            app.OpenButton_2.Enable = 'off';
            app.OpenButton_2.Position = [170 19 100 22];
            app.OpenButton_2.Text = 'Open';

            % Create ListBoxLabel
            app.ListBoxLabel = uilabel(app.WindowFunctionButtonGroup);
            app.ListBoxLabel.VerticalAlignment = 'top';
            app.ListBoxLabel.Position = [140 155 25 15];
            app.ListBoxLabel.Text = '';

            % Create WindowList
            app.WindowList = uilistbox(app.WindowFunctionButtonGroup);
            app.WindowList.Items = {'Barthann', 'Bartlett', 'Blackman', 'Blackman - Harris', 'Bohman', 'Chebyshev', 'Flat Top', 'Gaussian', 'Hamming', 'Hann', 'Kaiser', 'Nuttall', 'Parzen', 'Rectangular', 'Taylor', 'Triangular', 'Tukey'};
            app.WindowList.Position = [140 98 130 74];
            app.WindowList.Value = 'Barthann';

            % Create WindowdurationsSpinnerLabel
            app.WindowdurationsSpinnerLabel = uilabel(app.WindowFunctionButtonGroup);
            app.WindowdurationsSpinnerLabel.HorizontalAlignment = 'right';
            app.WindowdurationsSpinnerLabel.VerticalAlignment = 'top';
            app.WindowdurationsSpinnerLabel.Position = [11 70 114 15];
            app.WindowdurationsSpinnerLabel.Text = 'Window duration (s)';

            % Create WindowDuration
            app.WindowDuration = uispinner(app.WindowFunctionButtonGroup);
            app.WindowDuration.Limits = [0 Inf];
            app.WindowDuration.Position = [197 66 73 22];

            % Create AmplitudeSpinner_2Label
            app.AmplitudeSpinner_2Label = uilabel(app.WindowedSinusoidalTab);
            app.AmplitudeSpinner_2Label.HorizontalAlignment = 'right';
            app.AmplitudeSpinner_2Label.VerticalAlignment = 'top';
            app.AmplitudeSpinner_2Label.Position = [21 253 60 15];
            app.AmplitudeSpinner_2Label.Text = 'Amplitude';

            % Create WindowedSinusoidalAmplitude
            app.WindowedSinusoidalAmplitude = uispinner(app.WindowedSinusoidalTab);
            app.WindowedSinusoidalAmplitude.Position = [96 249 100 22];

            % Create FrequencyHzLabel_4
            app.FrequencyHzLabel_4 = uilabel(app.WindowedSinusoidalTab);
            app.FrequencyHzLabel_4.HorizontalAlignment = 'center';
            app.FrequencyHzLabel_4.VerticalAlignment = 'top';
            app.FrequencyHzLabel_4.Position = [18 190 66 28];
            app.FrequencyHzLabel_4.Text = {'Frequency '; '(Hz)'};

            % Create WindowedSinusoidalFrequency
            app.WindowedSinusoidalFrequency = uispinner(app.WindowedSinusoidalTab);
            app.WindowedSinusoidalFrequency.Limits = [0 Inf];
            app.WindowedSinusoidalFrequency.Position = [96 193 100 22];

            % Create PhaseLabel_3
            app.PhaseLabel_3 = uilabel(app.WindowedSinusoidalTab);
            app.PhaseLabel_3.HorizontalAlignment = 'right';
            app.PhaseLabel_3.VerticalAlignment = 'top';
            app.PhaseLabel_3.Position = [25 136 56 15];
            app.PhaseLabel_3.Text = 'Phase (°)';

            % Create WindowedSinusoidalPhase
            app.WindowedSinusoidalPhase = uispinner(app.WindowedSinusoidalTab);
            app.WindowedSinusoidalPhase.Position = [96 132 100 22];

            % Create GenerateWindowedSinusoidal
            app.GenerateWindowedSinusoidal = uibutton(app.WindowedSinusoidalTab, 'push');
            app.GenerateWindowedSinusoidal.ButtonPushedFcn = createCallbackFcn(app, @GenerateWindowedSinusoidalButtonPushed, true);
            app.GenerateWindowedSinusoidal.Position = [375 24 100 22];
            app.GenerateWindowedSinusoidal.Text = 'Generate';

            % Create StartingtimesLabel
            app.StartingtimesLabel = uilabel(app.WindowedSinusoidalTab);
            app.StartingtimesLabel.HorizontalAlignment = 'center';
            app.StartingtimesLabel.VerticalAlignment = 'top';
            app.StartingtimesLabel.Position = [34 74 50 28];
            app.StartingtimesLabel.Text = {'Starting '; 'time (s)'};

            % Create StartTime
            app.StartTime = uispinner(app.WindowedSinusoidalTab);
            app.StartTime.Limits = [0 Inf];
            app.StartTime.Position = [96 77 100 22];

            % Create RectangleWindowedLinearChirpTab
            app.RectangleWindowedLinearChirpTab = uitab(app.TabGroup);
            app.RectangleWindowedLinearChirpTab.AutoResizeChildren = 'off';
            app.RectangleWindowedLinearChirpTab.Title = 'Rectangle Windowed Linear Chirp';

            % Create PhaseLabel_2
            app.PhaseLabel_2 = uilabel(app.RectangleWindowedLinearChirpTab);
            app.PhaseLabel_2.HorizontalAlignment = 'right';
            app.PhaseLabel_2.VerticalAlignment = 'top';
            app.PhaseLabel_2.Position = [25 136 56 15];
            app.PhaseLabel_2.Text = 'Phase (°)';

            % Create LinearChirpPhase
            app.LinearChirpPhase = uispinner(app.RectangleWindowedLinearChirpTab);
            app.LinearChirpPhase.Position = [96 132 100 22];

            % Create BandwidthHzLabel
            app.BandwidthHzLabel = uilabel(app.RectangleWindowedLinearChirpTab);
            app.BandwidthHzLabel.HorizontalAlignment = 'center';
            app.BandwidthHzLabel.VerticalAlignment = 'top';
            app.BandwidthHzLabel.Position = [18 190 63 28];
            app.BandwidthHzLabel.Text = {'Bandwidth'; '(Hz)'};

            % Create LinearChirpBandwidth
            app.LinearChirpBandwidth = uispinner(app.RectangleWindowedLinearChirpTab);
            app.LinearChirpBandwidth.Position = [96 193 100 22];

            % Create AmplitudeSpinner_7Label
            app.AmplitudeSpinner_7Label = uilabel(app.RectangleWindowedLinearChirpTab);
            app.AmplitudeSpinner_7Label.HorizontalAlignment = 'right';
            app.AmplitudeSpinner_7Label.VerticalAlignment = 'top';
            app.AmplitudeSpinner_7Label.Position = [21 253 60 15];
            app.AmplitudeSpinner_7Label.Text = 'Amplitude';

            % Create LinearChirpAmplitude
            app.LinearChirpAmplitude = uispinner(app.RectangleWindowedLinearChirpTab);
            app.LinearChirpAmplitude.Position = [96 249 100 22];

            % Create GenerateLinearChirp
            app.GenerateLinearChirp = uibutton(app.RectangleWindowedLinearChirpTab, 'push');
            app.GenerateLinearChirp.ButtonPushedFcn = createCallbackFcn(app, @GenerateLinearChirpButtonPushed, true);
            app.GenerateLinearChirp.Position = [375 24 100 22];
            app.GenerateLinearChirp.Text = 'Generate';

            % Create InitialinstantenousfrequencyHzLabel
            app.InitialinstantenousfrequencyHzLabel = uilabel(app.RectangleWindowedLinearChirpTab);
            app.InitialinstantenousfrequencyHzLabel.HorizontalAlignment = 'center';
            app.InitialinstantenousfrequencyHzLabel.Position = [250 246 110 28];
            app.InitialinstantenousfrequencyHzLabel.Text = {'Initial instantenous '; 'frequency (Hz)'};

            % Create LinearChirpInitial
            app.LinearChirpInitial = uispinner(app.RectangleWindowedLinearChirpTab);
            app.LinearChirpInitial.Position = [375 249 100 22];

            % Create DurationSpinnerLabel
            app.DurationSpinnerLabel = uilabel(app.RectangleWindowedLinearChirpTab);
            app.DurationSpinnerLabel.HorizontalAlignment = 'right';
            app.DurationSpinnerLabel.VerticalAlignment = 'top';
            app.DurationSpinnerLabel.Position = [308 197 52 15];
            app.DurationSpinnerLabel.Text = 'Duration';

            % Create LinearChirpDuration
            app.LinearChirpDuration = uispinner(app.RectangleWindowedLinearChirpTab);
            app.LinearChirpDuration.Position = [375 193 100 22];

            % Create TimeshiftSpinnerLabel
            app.TimeshiftSpinnerLabel = uilabel(app.RectangleWindowedLinearChirpTab);
            app.TimeshiftSpinnerLabel.HorizontalAlignment = 'right';
            app.TimeshiftSpinnerLabel.VerticalAlignment = 'top';
            app.TimeshiftSpinnerLabel.Position = [303 136 57 15];
            app.TimeshiftSpinnerLabel.Text = 'Time shift';

            % Create LinearChirpTimeshift
            app.LinearChirpTimeshift = uispinner(app.RectangleWindowedLinearChirpTab);
            app.LinearChirpTimeshift.Position = [375 132 100 22];

            % Create MultipleSinusoidalTab
            app.MultipleSinusoidalTab = uitab(app.TabGroup);
            app.MultipleSinusoidalTab.AutoResizeChildren = 'off';
            app.MultipleSinusoidalTab.Title = 'Multiple Sinusoidal';

            % Create MultipleSinusoidalTable
            app.MultipleSinusoidalTable = uitable(app.MultipleSinusoidalTab);
            app.MultipleSinusoidalTable.ColumnName = {'Amplitude'; 'Frequency (Hz)'; 'Phase (°)'};
            app.MultipleSinusoidalTable.RowName = {};
            app.MultipleSinusoidalTable.ColumnEditable = true;
            app.MultipleSinusoidalTable.RowStriping = 'off';
            app.MultipleSinusoidalTable.Position = [32 113 302 185];

            % Create AddButton
            app.AddButton = uibutton(app.MultipleSinusoidalTab, 'push');
            app.AddButton.ButtonPushedFcn = createCallbackFcn(app, @AddButtonPushed, true);
            app.AddButton.Position = [370 253 100 22];
            app.AddButton.Text = 'Add';

            % Create RemoveButton
            app.RemoveButton = uibutton(app.MultipleSinusoidalTab, 'push');
            app.RemoveButton.ButtonPushedFcn = createCallbackFcn(app, @RemoveButtonPushed, true);
            app.RemoveButton.Position = [370 213 100 22];
            app.RemoveButton.Text = 'Remove';

            % Create GenerateMultipleSinusoidal
            app.GenerateMultipleSinusoidal = uibutton(app.MultipleSinusoidalTab, 'push');
            app.GenerateMultipleSinusoidal.ButtonPushedFcn = createCallbackFcn(app, @GenerateMultipleSinusoidalButtonPushed, true);
            app.GenerateMultipleSinusoidal.Position = [375 24 100 22];
            app.GenerateMultipleSinusoidal.Text = 'Generate';

            % Create SamplingfrequencyHzSpinnerLabel
            app.SamplingfrequencyHzSpinnerLabel = uilabel(app.DataGenerationTab);
            app.SamplingfrequencyHzSpinnerLabel.HorizontalAlignment = 'right';
            app.SamplingfrequencyHzSpinnerLabel.Position = [29 128 140 15];
            app.SamplingfrequencyHzSpinnerLabel.Text = 'Sampling frequency (Hz)';

            % Create SamplingfrequencyHzSpinner
            app.SamplingfrequencyHzSpinner = uispinner(app.DataGenerationTab);
            app.SamplingfrequencyHzSpinner.Limits = [1 Inf];
            app.SamplingfrequencyHzSpinner.Position = [182 124 100 22];
            app.SamplingfrequencyHzSpinner.Value = 1;

            % Create DurationsSpinnerLabel
            app.DurationsSpinnerLabel = uilabel(app.DataGenerationTab);
            app.DurationsSpinnerLabel.HorizontalAlignment = 'right';
            app.DurationsSpinnerLabel.VerticalAlignment = 'top';
            app.DurationsSpinnerLabel.Position = [98 163 69 15];
            app.DurationsSpinnerLabel.Text = 'Duration (s)';

            % Create DurationsSpinner
            app.DurationsSpinner = uispinner(app.DataGenerationTab);
            app.DurationsSpinner.Limits = [0 Inf];
            app.DurationsSpinner.Position = [182 159 100 22];

            % Create GeneratedSignalTimeDomain
            app.GeneratedSignalTimeDomain = uiaxes(app.DataGenerationTab);
            title(app.GeneratedSignalTimeDomain, 'Time Domain Signal')
            xlabel(app.GeneratedSignalTimeDomain, 't')
            ylabel(app.GeneratedSignalTimeDomain, 'x(t)')
            app.GeneratedSignalTimeDomain.XGrid = 'on';
            app.GeneratedSignalTimeDomain.YGrid = 'on';
            app.GeneratedSignalTimeDomain.Box = 'on';
            app.GeneratedSignalTimeDomain.Position = [549 310 332 282];

            % Create GeneratedSignalFrequencyDomain
            app.GeneratedSignalFrequencyDomain = uiaxes(app.DataGenerationTab);
            title(app.GeneratedSignalFrequencyDomain, 'Frequency Domain Signal')
            xlabel(app.GeneratedSignalFrequencyDomain, 'Frequency (Hz)')
            ylabel(app.GeneratedSignalFrequencyDomain, '| X[k] |')
            app.GeneratedSignalFrequencyDomain.XGrid = 'on';
            app.GeneratedSignalFrequencyDomain.YGrid = 'on';
            app.GeneratedSignalFrequencyDomain.Box = 'on';
            app.GeneratedSignalFrequencyDomain.Position = [549 10 332 282];

            % Create SpectrogramTab
            app.SpectrogramTab = uitab(app.TabGroup2);
            app.SpectrogramTab.AutoResizeChildren = 'off';
            app.SpectrogramTab.Title = 'Spectrogram';

            % Create InputSignalButtonGroup
            app.InputSignalButtonGroup = uibuttongroup(app.SpectrogramTab);
            app.InputSignalButtonGroup.AutoResizeChildren = 'off';
            app.InputSignalButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @InputSignalButtonGroupSelectionChanged, true);
            app.InputSignalButtonGroup.Title = 'Input Signal';
            app.InputSignalButtonGroup.Position = [735 495 187 84];

            % Create UseacquiredsignalButton
            app.UseacquiredsignalButton = uiradiobutton(app.InputSignalButtonGroup);
            app.UseacquiredsignalButton.Text = 'Use acquired signal';
            app.UseacquiredsignalButton.Position = [11 38 131 15];
            app.UseacquiredsignalButton.Value = true;

            % Create UsegeneratedsignalButton
            app.UsegeneratedsignalButton = uiradiobutton(app.InputSignalButtonGroup);
            app.UsegeneratedsignalButton.Text = 'Use generated signal';
            app.UsegeneratedsignalButton.Position = [11 16 139 15];

            % Create WindowSignalPanel
            app.WindowSignalPanel = uipanel(app.SpectrogramTab);
            app.WindowSignalPanel.AutoResizeChildren = 'off';
            app.WindowSignalPanel.Title = 'Window Signal';
            app.WindowSignalPanel.Position = [735 235 187 243];

            % Create WindowTypeLabel
            app.WindowTypeLabel = uilabel(app.WindowSignalPanel);
            app.WindowTypeLabel.VerticalAlignment = 'top';
            app.WindowTypeLabel.Position = [12 176 79 15];
            app.WindowTypeLabel.Text = 'Window Type';

            % Create WindowList_2
            app.WindowList_2 = uilistbox(app.WindowSignalPanel);
            app.WindowList_2.Items = {'Barthann', 'Bartlett', 'Blackman', 'Blackman - Harris', 'Bohman', 'Chebyshev', 'Flat Top', 'Gaussian', 'Hamming', 'Hann', 'Kaiser', 'Nuttall', 'Parzen', 'Rectangular', 'Taylor', 'Triangular', 'Tukey'};
            app.WindowList_2.Position = [12 119 167 74];
            app.WindowList_2.Value = 'Barthann';

            % Create WindowSampleSizeLabel
            app.WindowSampleSizeLabel = uilabel(app.WindowSignalPanel);
            app.WindowSampleSizeLabel.HorizontalAlignment = 'center';
            app.WindowSampleSizeLabel.Position = [12 60 50 42];
            app.WindowSampleSizeLabel.Text = {'Window'; 'Length '};

            % Create WindowSampleSizeSpinner
            app.WindowSampleSizeSpinner = uispinner(app.WindowSignalPanel);
            app.WindowSampleSizeSpinner.Limits = [1 Inf];
            app.WindowSampleSizeSpinner.Position = [77 72 100 22];
            app.WindowSampleSizeSpinner.Value = 1;

            % Create WindowOverlapSpinnerLabel
            app.WindowOverlapSpinnerLabel = uilabel(app.WindowSignalPanel);
            app.WindowOverlapSpinnerLabel.HorizontalAlignment = 'right';
            app.WindowOverlapSpinnerLabel.VerticalAlignment = 'top';
            app.WindowOverlapSpinnerLabel.Position = [12 23 49 28];
            app.WindowOverlapSpinnerLabel.Text = {'Window'; 'Overlap'};

            % Create WindowOverlapSpinner
            app.WindowOverlapSpinner = uispinner(app.WindowSignalPanel);
            app.WindowOverlapSpinner.Position = [77 26 100 22];

            % Create PlotButton
            app.PlotButton = uibutton(app.SpectrogramTab, 'push');
            app.PlotButton.ButtonPushedFcn = createCallbackFcn(app, @PlotButtonPushed, true);
            app.PlotButton.Enable = 'off';
            app.PlotButton.Position = [812 62 100 22];
            app.PlotButton.Text = 'Plot';

            % Create SpectrogramPlot
            app.SpectrogramPlot = uiaxes(app.SpectrogramTab);
            title(app.SpectrogramPlot, 'Spectrogram')
            xlabel(app.SpectrogramPlot, 'Time (secs)')
            ylabel(app.SpectrogramPlot, 'Frequency (Hz)')
            app.SpectrogramPlot.Position = [44 62 608 500];

            % Show the figure after all components are created
            app.Spectogram.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = Spectrogram

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.Spectogram)

            % Execute the startup function
            runStartupFcn(app, @startupFcn)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.Spectogram)
        end
    end
end