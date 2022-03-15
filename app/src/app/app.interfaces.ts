export interface ApiResponseInterface<T> { // <T[]> if a list is expected
  result?: T;
  error?: {
    type: string | number,
    message: string
  };
}

export interface LocationInterface {
  lat: number,
  lng: number
}

export interface IntervalInterFace {
  start: Date,
  end: Date,
  duration?: number
}

export interface TemperaturesInterface {
  morn: number;
  day: number;
  eve: number;
  night: number;
  min: number;
  max: number;
}

export interface FeelsLikeInterface {
  morn: number;
  day: number;
  eve: number;
  night: number;
}

export interface WeatherInterface {
  id: number;
  main: string;
  description: string;
  icon: string;
}

export interface ForecastInterface {
    location: LocationInterface;
    datetime: Date;
    temperatures: TemperaturesInterface;
    feels_like: FeelsLikeInterface;
    pressure: number;
    humidity: number;
    wind_speed: number;
    weather: WeatherInterface[];
}

export interface TextValueInterface {
  text: string;
  value: number;
}

export interface StepInterface {
  distance?: TextValueInterface;
  duration: TextValueInterface;
  end_location: LocationInterface;
  html_instructions: string;
  maneuver?: string;
  polyline: { points: string; };
  start_location: LocationInterface;
  travel_mode: string;
  steps?: StepInterface;
  transit_details?: ""; // TODO: specify
}

export interface ItineraryInterface {
  start_location: LocationInterface;
  end_location: LocationInterface;
  interval: IntervalInterFace;
  distance: number;
  steps: StepInterface[];
  walk_duration: number;
  travel_duration: number;
}

export interface databaseInterface {
  id: number;
  created: Date;
  updated: Date;
}

export interface SolutionInfoInterface {
  walk_duration: number;
  travel_duration: number;
  total_trip_duration: number;
  free_time: number;
}

export interface SolutionInterface extends databaseInterface {
  start_location: LocationInterface;
  query_id: number;
  place_id?: number;
  user_id?: number;
  interval: number;
  outward_itinerary: ItineraryInterface;
  return_itinerary: ItineraryInterface;
  forecasts: ForecastInterface[];
  info: SolutionInfoInterface;
}

export interface PartnerInterface extends databaseInterface {
  name: string;
  location: LocationInterface;
  types: string[];
  review_count: number;
  average_rating: number;
  query_count: number;
}

export interface PlaceInterface extends databaseInterface {
  location: LocationInterface;
  name: string;
  difficulty?: number;
  duration?: number;
  distance?: number;
  types?: string[];
  review_count: number;
  average_rating: number;
  query_count: number;
}

export interface QueryInterface extends databaseInterface {
  location: LocationInterface;
  interval: IntervalInterFace;
  radius: number;
  types: string[];
  max_travel: number;
  max_walk: number;
  weather_ids: number[];
  max_results: number;
  language?: string;
  favorited: boolean;
  user_id?: number;
}

export interface ReviewInterface extends databaseInterface {
  rating: number;
  comment: string;
  user_id?: number;
  parent_id?: number;
  partner_id?: number;
  place_id?: number;
}

export interface UserInterface extends databaseInterface {
  email: string;
  password: string;
  confirmed: boolean;
  role: string;
  name: string;
  points: number;
}

export interface UserSessionDataInterface {
  id: number;
  email: string;
  name: string;
  points: number;
  token?: string;
}