using System.Net.Http.Json;
using System.Text.Json;

namespace ContabilidadPanama.Frontend.Services;

public class ApiService
{
    private readonly HttpClient _http;
    private readonly JsonSerializerOptions _jsonOptions;

    public ApiService(HttpClient http)
    {
        _http = http;
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
    }

    private string _baseUrl = "https://api.contapanama.rsanjur.com";

    public async Task<T?> GetAsync<T>(string endpoint)
    {
        try
        {
            var response = await _http.GetAsync($"{_baseUrl}{endpoint}");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<T>(_jsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"API GET Error: {ex.Message}");
            return default;
        }
    }

    public async Task<T?> PostAsync<T>(string endpoint, object data)
    {
        try
        {
            var response = await _http.PostAsJsonAsync($"{_baseUrl}{endpoint}", data, _jsonOptions);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<T>(_jsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"API POST Error: {ex.Message}");
            return default;
        }
    }

    public async Task<T?> PutAsync<T>(string endpoint, object data)
    {
        try
        {
            var response = await _http.PutAsJsonAsync($"{_baseUrl}{endpoint}", data, _jsonOptions);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<T>(_jsonOptions);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"API PUT Error: {ex.Message}");
            return default;
        }
    }

    public async Task<bool> DeleteAsync(string endpoint)
    {
        try
        {
            var response = await _http.DeleteAsync($"{_baseUrl}{endpoint}");
            return response.IsSuccessStatusCode;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"API DELETE Error: {ex.Message}");
            return false;
        }
    }
}

public class DashboardData
{
    public int TotalClientes { get; set; }
    public int TotalProveedores { get; set; }
    public int TotalProductos { get; set; }
    public int TotalEmpleados { get; set; }
    public double VentasMes { get; set; }
    public double GastosMes { get; set; }
    public double IngresosMes { get; set; }
    public double BancosTotal { get; set; }
}

public class InvoiceDto
{
    public int Id { get; set; }
    public string Number { get; set; } = "";
    public string Type { get; set; } = "";
    public string Status { get; set; } = "";
    public DateTime IssueDate { get; set; }
    public string ReceiverRuc { get; set; } = "";
    public string ReceiverRazonSocial { get; set; } = "";
    public double Subtotal { get; set; }
    public double Itbms { get; set; }
    public double Total { get; set; }
}

public class ClientDto
{
    public int Id { get; set; }
    public string Ruc { get; set; } = "";
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public string Phone { get; set; } = "";
    public string Address { get; set; } = "";
}

public class ProductDto
{
    public int Id { get; set; }
    public string Code { get; set; } = "";
    public string Name { get; set; } = "";
    public double CostPrice { get; set; }
    public double SalePrice { get; set; }
    public double Stock { get; set; }
}

public class ExpenseDto
{
    public int Id { get; set; }
    public string Description { get; set; } = "";
    public double TotalAmount { get; set; }
    public DateTime ExpenseDate { get; set; }
    public string Status { get; set; } = "";
}

public class EmployeeDto
{
    public int Id { get; set; }
    public string Cedula { get; set; } = "";
    public string Nombre { get; set; } = "";
    public string Apellido { get; set; } = "";
    public string Cargo { get; set; } = "";
    public double SalarioBase { get; set; }
}
