using System.ComponentModel;
using Microsoft.JSInterop;
using MudBlazor;

namespace ContabilidadPanama.Frontend.Services;

public class ThemeService : INotifyPropertyChanged
{
    private readonly IJSRuntime _js;
    private bool _isDarkMode;
    
    public event PropertyChangedEventHandler? PropertyChanged;
    
    public bool IsDarkMode 
    { 
        get => _isDarkMode;
        set 
        {
            if (_isDarkMode != value)
            {
                _isDarkMode = value;
                UpdateTheme();
                OnPropertyChanged(nameof(IsDarkMode));
                OnPropertyChanged(nameof(CurrentTheme));
            }
        }
    }

    public MudTheme CurrentTheme { get; private set; }

    public ThemeService(IJSRuntime js)
    {
        _js = js;
        CurrentTheme = CreateLightTheme();
    }

    public void ToggleTheme()
    {
        IsDarkMode = !IsDarkMode;
    }

    public async Task LoadPreferenceAsync()
    {
        try
        {
            var isDark = await _js.InvokeAsync<string>("localStorage.getItem", "theme");
            _isDarkMode = isDark == "dark";
            UpdateTheme();
            OnPropertyChanged(nameof(IsDarkMode));
            OnPropertyChanged(nameof(CurrentTheme));
        }
        catch
        {
            _isDarkMode = false;
            UpdateTheme();
        }
    }

    public async Task SavePreferenceAsync()
    {
        try
        {
            await _js.InvokeVoidAsync("localStorage.setItem", "theme", _isDarkMode ? "dark" : "light");
        }
        catch { }
    }

    private void UpdateTheme()
    {
        CurrentTheme = _isDarkMode ? CreateDarkTheme() : CreateLightTheme();
    }

    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private MudTheme CreateLightTheme() => new MudTheme
    {
        PaletteLight = new PaletteLight
        {
            Primary = "#2563EB",
            Secondary = "#7C3AED",
            Tertiary = "#10B981",
            Info = "#3B82F6",
            Success = "#10B981",
            Warning = "#F59E0B",
            Error = "#EF4444",
            AppbarBackground = "#FFFFFF",
            AppbarText = "#1E293B",
            Background = "#F8FAFC",
            Surface = "#FFFFFF",
            TextPrimary = "#0F172A",
            TextSecondary = "#64748B",
            DrawerBackground = "#FFFFFF",
            DrawerText = "#334155",
            DrawerIcon = "#64748B",
            Divider = "#E2E8F0",
        },
        LayoutProperties = new LayoutProperties
        {
            AppbarHeight = "64px",
        }
    };

    private MudTheme CreateDarkTheme() => new MudTheme
    {
        PaletteDark = new PaletteDark
        {
            Primary = "#3B82F6",
            Secondary = "#8B5CF6",
            Tertiary = "#34D399",
            Info = "#60A5FA",
            Success = "#34D399",
            Warning = "#FBBF24",
            Error = "#F87171",
            AppbarBackground = "#1E293B",
            AppbarText = "#F1F5F9",
            Background = "#0F172A",
            Surface = "#1E293B",
            TextPrimary = "#F1F5F9",
            TextSecondary = "#94A3B8",
            DrawerBackground = "#1E293B",
            DrawerText = "#E2E8F0",
            DrawerIcon = "#94A3B8",
            Divider = "#334155",
        },
        LayoutProperties = new LayoutProperties
        {
            AppbarHeight = "64px",
        }
    };
}
