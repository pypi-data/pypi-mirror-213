#  Copyright 2022 Dmytro Stepanenko, Granny Pliers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""ConfusionMatrix"""

from dataclasses import dataclass

__all__ = ["ConfusionMatrix"]


@dataclass()
class ConfusionMatrix:
    """ConfusionMatrix"""

    true_positive: int = 0
    """Predicted positive and its positive"""

    true_negative: int = 0
    """Predicted negative and its negative"""

    false_positive: int = 0
    """Predicted positive but its negative"""

    false_negative: int = 0
    """Predicted negative but its positive"""

    def increment(self, predicted: bool, actual: bool):
        """increment"""
        match predicted:
            case True:
                match actual:
                    case True:
                        self.true_positive += 1
                    case False:
                        self.false_positive += 1
            case False:
                match actual:
                    case False:
                        self.true_negative += 1
                    case True:
                        self.false_negative += 1

    def __str__(self):
        return (
            "A: {accuracy}\t| TP: {tp}\t| TN: {tn}\t| FP: {fp}\t| FN: {fn}\t\t| T: {total}\t| "
            "P: {precision}\t| R: {recall}".format(
                tp=self.true_positive,
                fp=self.false_positive,
                fn=self.false_negative,
                tn=self.true_negative,
                total=self.total,
                accuracy=round(self.accuracy, 4),
                precision=round(self.precision, 4),
                recall=round(self.recall, 4),
            )
        )

    @property
    def total(self) -> int:
        """total"""
        return self.true_positive + self.true_negative + self.false_positive + self.false_negative

    @property
    def accuracy(self) -> float:
        """accuracy"""
        return (self.true_positive + self.true_negative) / max(self.total, 1)

    @property
    def recall(self) -> float:
        """recall"""
        return self.true_positive / max(self.true_positive + self.false_negative, 1)

    @property
    def precision(self) -> float:
        """precision"""
        return self.true_positive / max((self.true_positive + self.false_positive), 1)
