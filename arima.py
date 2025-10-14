import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings

warnings.filterwarnings('ignore')


def configure_logging():
    """Configure logging for the script with informative output."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def generate_synthetic_data(days=30, freq='1min', trend=0.01, seasonality_strength=2.0, noise_level=0.5):
    """Generate synthetic time series data with trend, seasonality, and noise.
    
    Args:
        days (int): Number of days of historical data
        freq (str): Frequency of data points (default: '1min' for minute-level)
        trend (float): Linear trend coefficient
        seasonality_strength (float): Amplitude of seasonal component
        noise_level (float): Standard deviation of random noise
    
    Returns:
        pd.Series: Time series data with datetime index
    """
    logging.info(f"Generating {days} days of synthetic time series data...")
    
    # Create datetime index
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
    
    # Generate components
    n_points = len(date_range)
    time_index = np.arange(n_points)
    
    # Trend component
    trend_component = trend * time_index
    
    # Seasonal component (daily pattern with 1440 minutes per day)
    seasonal_component = seasonality_strength * np.sin(2 * np.pi * time_index / 1440)
    
    # Weekly pattern (7 days * 1440 minutes)
    weekly_component = 0.5 * seasonality_strength * np.sin(2 * np.pi * time_index / (7 * 1440))
    
    # Random noise
    noise = np.random.normal(0, noise_level, n_points)
    
    # Combine components
    values = 50 + trend_component + seasonal_component + weekly_component + noise
    
    # Create time series
    time_series = pd.Series(values, index=date_range)
    
    logging.info(f"Generated {len(time_series)} data points")
    return time_series


def fit_arima_model(time_series, order=(5, 1, 2)):
    """Fit ARIMA model to time series data.
    
    Args:
        time_series (pd.Series): Time series data
        order (tuple): ARIMA order (p, d, q)
    
    Returns:
        ARIMAResults: Fitted ARIMA model
    """
    try:
        logging.info(f"Fitting ARIMA{order} model...")
        model = ARIMA(time_series, order=order)
        fitted_model = model.fit()
        logging.info(f"Model fitted successfully - AIC: {fitted_model.aic:.2f}")
        return fitted_model
    except Exception as e:
        logging.error(f"Error fitting ARIMA model: {e}")
        raise


def forecast_future(fitted_model, steps=10):
    """Generate forecasts for future time periods.
    
    Args:
        fitted_model (ARIMAResults): Fitted ARIMA model
        steps (int): Number of steps to forecast
    
    Returns:
        tuple: (forecast, confidence_interval)
    """
    try:
        logging.info(f"Forecasting next {steps} time steps...")
        forecast_result = fitted_model.forecast(steps=steps)
        conf_int = fitted_model.get_forecast(steps=steps).conf_int()
        
        logging.info("Forecast completed successfully")
        return forecast_result, conf_int
    except Exception as e:
        logging.error(f"Error generating forecast: {e}")
        raise


def plot_results(historical_data, forecast, conf_int, lookback_points=1440):
    """Visualize historical data, forecast, and confidence intervals.
    
    Args:
        historical_data (pd.Series): Historical time series data
        forecast (pd.Series): Forecasted values
        conf_int (pd.DataFrame): Confidence intervals
        lookback_points (int): Number of recent points to display
    """
    logging.info("Creating visualization...")
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Time series with forecast
    ax1 = axes[0]
    recent_data = historical_data.iloc[-lookback_points:]
    
    # Create forecast index
    last_date = historical_data.index[-1]
    forecast_index = pd.date_range(
        start=last_date + timedelta(minutes=1),
        periods=len(forecast),
        freq='1min'
    )
    
    # Plot historical data
    ax1.plot(recent_data.index, recent_data.values, 
             label='Historical Data', color='#2E86AB', linewidth=1.5)
    
    # Plot forecast
    ax1.plot(forecast_index, forecast.values, 
             label='Forecast', color='#A23B72', linewidth=2, marker='o', markersize=4)
    
    # Plot confidence interval
    ax1.fill_between(forecast_index, 
                     conf_int.iloc[:, 0], 
                     conf_int.iloc[:, 1],
                     alpha=0.3, color='#F18F01', label='95% Confidence Interval')
    
    ax1.set_xlabel('Timestamp', fontsize=11)
    ax1.set_ylabel('Value', fontsize=11)
    ax1.set_title('ARIMA Time Series Forecast (Last 24 Hours + 10 Min Prediction)', 
                  fontsize=13, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot 2: Forecast detail view
    ax2 = axes[1]
    context_points = 60  # Show last hour for context
    context_data = historical_data.iloc[-context_points:]
    
    ax2.plot(context_data.index, context_data.values,
             label='Last Hour', color='#2E86AB', linewidth=1.5)
    ax2.plot(forecast_index, forecast.values,
             label='10 Min Forecast', color='#A23B72', linewidth=2, marker='o', markersize=5)
    ax2.fill_between(forecast_index,
                     conf_int.iloc[:, 0],
                     conf_int.iloc[:, 1],
                     alpha=0.3, color='#F18F01')
    
    ax2.set_xlabel('Timestamp', fontsize=11)
    ax2.set_ylabel('Value', fontsize=11)
    ax2.set_title('Detailed View: Last Hour + 10 Min Forecast', 
                  fontsize=13, fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    logging.info("Visualization created successfully")
    return fig


def main():
    """Main execution function for ARIMA forecasting pipeline."""
    configure_logging()
    
    try:
        # Generate synthetic data (30 days, minute-level)
        time_series = generate_synthetic_data(days=30, freq='1min')
        
        # Fit ARIMA model
        fitted_model = fit_arima_model(time_series, order=(5, 1, 2))
        
        # Forecast next 10 minutes
        forecast, conf_int = forecast_future(fitted_model, steps=10)
        
        # Display forecast results
        logging.info("\n" + "="*50)
        logging.info("FORECAST RESULTS (Next 10 Minutes)")
        logging.info("="*50)
        for i, (timestamp, value) in enumerate(forecast.items(), 1):
            lower_bound = conf_int.iloc[i-1, 0]
            upper_bound = conf_int.iloc[i-1, 1]
            logging.info(f"T+{i}: {value:.2f} (95% CI: [{lower_bound:.2f}, {upper_bound:.2f}])")
        
        # Visualize results
        fig = plot_results(time_series, forecast, conf_int)
        plt.show()
        
        logging.info("\nForecasting pipeline completed successfully!")
        
    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")
        raise


if __name__ == "__main__":
    main()