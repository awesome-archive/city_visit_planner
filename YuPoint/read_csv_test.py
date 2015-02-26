import datetime
import tempfile
import unittest

from Yusi.YuPoint.read_csv import ReadCSV, ReadCSVToDict, ExtractOperatingHours,\
  ExtractCoordinates
from Yusi.YuPoint.point import OperatingHours, Coordinates, Point, PointType,\
  PointAgeGroup


class ReadCSVTest(unittest.TestCase):

  def testExtractCoordinatesGeneral(self):
    ferry_building_coordinates = ExtractCoordinates('37.7955N, 122.3937W')
    self.assertEqual(Coordinates(37.7955, -122.3937),
                     ferry_building_coordinates)

    ferry_building_coordinates = ExtractCoordinates('37.7955, -122.3937')
    self.assertEqual(Coordinates(37.7955, -122.3937),
                     ferry_building_coordinates)

    kremlin_coordinates = ExtractCoordinates('55.7517N, 37.6178E')
    self.assertEqual(Coordinates(55.7517, 37.6178), kremlin_coordinates)

    kremlin_coordinates = ExtractCoordinates('55.7517, 37.6178')
    self.assertEqual(Coordinates(55.7517, 37.6178), kremlin_coordinates)

    christ_the_redeemer_coordinates = ExtractCoordinates('22.9519S, 43.2106W')
    self.assertEqual(Coordinates(-22.9519, -43.2106),
                     christ_the_redeemer_coordinates)

    christ_the_redeemer_coordinates = ExtractCoordinates('-22.9519, -43.2106')
    self.assertEqual(Coordinates(-22.9519, -43.2106),
                     christ_the_redeemer_coordinates)

    self.assertEqual(None, ExtractCoordinates(''))

  def testExtractOperatingHoursGeneral(self):
    de_young_museum_operating_hours = (
        ExtractOperatingHours('9:30:00', '17:15:00'))
    self.assertEqual(OperatingHours(datetime.time(9, 30, 0),
                                    datetime.time(17, 15, 0)),
                     de_young_museum_operating_hours)

  def testReadCSVGeneral(self):
    s = str()
    s += 'ID,Name,CoordinatesStarts,CoordinatesEnds,OperatingHoursOpens,OperatingHoursCloses,Duration,City Tours,Landmarks,Nature,Museums,Shopping,Dining,Senior,Adult,Junior,Child,Toddlers,Price,Parking,Eating\n'
    s += '1,Ferry Building,"37.7955N, 122.3937W",,09:00:00,18:00:00,1,,100,,,,,90,90,40,70,,,,100\n'
    s += '2,Pier 39,"37.8100N, 122.4104W",,10:00:00,22:00:00,3,,100,,,30,60,70,70,70,90,,,,100\n'
    csv_filepath = tempfile.mktemp()
    with open(csv_filepath, 'w') as csv_file:
      csv_file.write(s)

    pier_39 = Point(
        name='Pier 39',
        coordinates_starts=Coordinates(37.8100, -122.4104),
        coordinates_ends=None,
        operating_hours=OperatingHours(
            datetime.time(10, 0, 0), datetime.time(22, 0, 0)),
        duration=3.,
        point_type=PointType(
            city_tours=None,
            landmarks=100,
            nature=None,
            museums=None,
            shopping=30,
            dining=60),
        point_age_group=PointAgeGroup(
            senior=70,
            adult=70,
            junior=70,
            child=90,
            toddlers=None),
        price=None,
        parking=None,
        eating=100)

    points = ReadCSV(csv_filepath)
    self.assertEqual(2, len(points))
    self.assertEqual(pier_39, points[1])
    points = ReadCSVToDict(csv_filepath)
    self.assertEqual(2, len(points))
    self.assertEqual(set(['Ferry Building', 'Pier 39']), set(points.keys()))
    self.assertEqual(pier_39, points['Pier 39'])
                     

if __name__ == '__main__':
    unittest.main()

