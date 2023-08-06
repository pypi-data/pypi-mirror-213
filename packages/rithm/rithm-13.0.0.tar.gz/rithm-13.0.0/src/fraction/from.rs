use traiter::numbers::One;

use super::types::Fraction;

impl<Component: One> From<Component> for Fraction<Component> {
    fn from(value: Component) -> Self {
        Self {
            numerator: value,
            denominator: Component::one(),
        }
    }
}
